(function () {
  function clone(value) {
    return JSON.parse(JSON.stringify(value || {}));
  }

  function recordTime(record) {
    const time = Date.parse(record?.updatedAt || "");
    return Number.isFinite(time) ? time : 0;
  }

  function mergeProgress(localProgress, cloudProgress) {
    const local = localProgress || {};
    const cloud = cloudProgress || {};
    const merged = {};
    const questionIds = new Set([...Object.keys(cloud), ...Object.keys(local)]);

    questionIds.forEach((questionId) => {
      const localRecord = local[questionId];
      const cloudRecord = cloud[questionId];

      if (!localRecord) {
        merged[questionId] = clone(cloudRecord);
        return;
      }

      if (!cloudRecord || recordTime(localRecord) >= recordTime(cloudRecord)) {
        merged[questionId] = clone(localRecord);
        return;
      }

      merged[questionId] = clone(cloudRecord);
    });

    return merged;
  }

  function sameProgress(left, right) {
    return JSON.stringify(left || {}) === JSON.stringify(right || {});
  }

  class CloudProgressService {
    constructor({ onStatus, onUserChange } = {}) {
      this.client = null;
      this.user = null;
      this.onStatus = onStatus || (() => {});
      this.onUserChange = onUserChange || (() => {});
      this.pending = new Map();
      this.timers = new Map();
      this.authSubscription = null;

      window.addEventListener("online", () => this.flushAll());
    }

    get config() {
      return window.GEO_CLOUD_CONFIG || {};
    }

    isConfigured() {
      const { supabaseUrl, supabaseAnonKey } = this.config;
      if (!window.supabase || !String(supabaseAnonKey || "").trim()) {
        return false;
      }

      try {
        return new URL(String(supabaseUrl || "").trim()).protocol === "https:";
      } catch {
        return false;
      }
    }

    isSignedIn() {
      return Boolean(this.user);
    }

    notify(status, message) {
      this.onStatus({ status, message, configured: this.isConfigured(), user: this.user });
    }

    async init() {
      if (!this.isConfigured()) {
        this.notify("local", "云同步尚未配置，当前进度仅保存在本机");
        return;
      }

      const { supabaseUrl, supabaseAnonKey } = this.config;
      this.client = window.supabase.createClient(supabaseUrl, supabaseAnonKey, {
        auth: {
          persistSession: true,
          autoRefreshToken: true,
          detectSessionInUrl: true,
        },
      });

      const {
        data: { session },
      } = await this.client.auth.getSession();
      this.user = session?.user || null;

      const { data } = this.client.auth.onAuthStateChange((_event, nextSession) => {
        const previousUserId = this.user?.id;
        this.user = nextSession?.user || null;
        this.notify(this.user ? "ready" : "local", this.user ? "已登录，正在同步" : "当前进度仅保存在本机");

        if (previousUserId !== this.user?.id) {
          this.onUserChange(this.user);
        }
      });
      this.authSubscription = data.subscription;
      this.notify(this.user ? "ready" : "local", this.user ? "已登录，正在同步" : "当前进度仅保存在本机");
    }

    async signIn(email, password) {
      if (!this.client) throw new Error("云同步尚未配置");
      const { data, error } = await this.client.auth.signInWithPassword({ email, password });
      if (error) throw error;
      this.user = data.user;
      this.notify("ready", "登录成功，正在恢复答题进度");
      return data.user;
    }

    async signUp(email, password) {
      if (!this.client) throw new Error("云同步尚未配置");
      const { data, error } = await this.client.auth.signUp({ email, password });
      if (error) throw error;
      if (data.session) {
        this.user = data.user;
        this.notify("ready", "注册成功，正在同步答题进度");
      }
      return data;
    }

    async signOut() {
      if (!this.client) return;
      const { error } = await this.client.auth.signOut();
      if (error) throw error;
      this.user = null;
      this.pending.clear();
      this.notify("local", "已退出，之后的进度仅保存在本机");
    }

    async loadProgress(bankId, localProgress) {
      if (!this.client || !this.user) return clone(localProgress);

      this.notify("syncing", "正在恢复云端进度");
      const { data, error } = await this.client
        .from("student_progress")
        .select("progress")
        .eq("user_id", this.user.id)
        .eq("bank_id", bankId)
        .maybeSingle();

      if (error) {
        this.notify("error", `云端读取失败：${error.message}`);
        return clone(localProgress);
      }

      const cloudProgress = data?.progress || {};
      const merged = mergeProgress(localProgress, cloudProgress);

      if (!sameProgress(merged, cloudProgress)) {
        await this.saveNow(bankId, merged);
      } else {
        this.notify("synced", "进度已同步");
      }

      return merged;
    }

    queueSave(bankId, progress) {
      if (!this.client || !this.user || !bankId) return;

      this.pending.set(bankId, clone(progress));
      clearTimeout(this.timers.get(bankId));
      this.notify("pending", navigator.onLine ? "正在保存进度" : "网络离线，恢复后自动同步");

      const timer = window.setTimeout(() => this.flushBank(bankId), 700);
      this.timers.set(bankId, timer);
    }

    async saveNow(bankId, progress) {
      if (!this.client || !this.user || !bankId) return false;

      if (!navigator.onLine) {
        this.pending.set(bankId, clone(progress));
        this.notify("pending", "网络离线，恢复后自动同步");
        return false;
      }

      const { data: currentData, error: readError } = await this.client
        .from("student_progress")
        .select("progress")
        .eq("user_id", this.user.id)
        .eq("bank_id", bankId)
        .maybeSingle();

      if (readError) {
        this.pending.set(bankId, clone(progress));
        this.notify("error", `云端保存前校验失败：${readError.message}`);
        return false;
      }

      const mergedProgress = mergeProgress(progress, currentData?.progress || {});
      const { error } = await this.client.from("student_progress").upsert(
        {
          user_id: this.user.id,
          bank_id: bankId,
          progress: mergedProgress,
          updated_at: new Date().toISOString(),
        },
        { onConflict: "user_id,bank_id" },
      );

      if (error) {
        this.pending.set(bankId, clone(progress));
        this.notify("error", `云端保存失败：${error.message}`);
        return false;
      }

      this.pending.delete(bankId);
      this.notify("synced", "进度已同步");
      return true;
    }

    async flushBank(bankId) {
      clearTimeout(this.timers.get(bankId));
      this.timers.delete(bankId);
      const progress = this.pending.get(bankId);
      if (!progress) return;
      await this.saveNow(bankId, progress);
    }

    async flushAll() {
      await Promise.all([...this.pending.keys()].map((bankId) => this.flushBank(bankId)));
    }
  }

  window.GeoCloud = {
    CloudProgressService,
    mergeProgress,
  };
})();
