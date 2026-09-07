(function () {
  "use strict";

  var form = document.getElementById("loginForm");
  var formAlert = document.getElementById("formAlert");
  var formNotice = document.getElementById("formNotice");
  var submitBtn = document.getElementById("submitBtn");
  var forgotPasswordLink = document.getElementById("forgotPasswordLink");

  var fields = {
    identifier: document.getElementById("identifier"),
    password: document.getElementById("password")
  };

  var isSubmitting = false;

  /* ========================================================================
     Helpers
     ======================================================================== */

  function setFieldError(name, message) {
    var el = document.getElementById("err_" + name);
    var input = fields[name];
    if (el) el.textContent = message || "";
    if (input) {
      if (message) {
        input.setAttribute("aria-invalid", "true");
      } else {
        input.removeAttribute("aria-invalid");
      }
    }
  }

  function clearAllErrors() {
    Object.keys(fields).forEach(function (name) { setFieldError(name, ""); });
  }

  function showAlert(message) {
    formAlert.textContent = message;
    formAlert.hidden = !message;
  }

  function showNotice(message) {
    formNotice.textContent = message;
    formNotice.hidden = !message;
  }

  function clearMessages() {
    showAlert("");
    showNotice("");
  }

  function setLoading(loading) {
    isSubmitting = loading;
    submitBtn.disabled = loading;
    submitBtn.querySelector(".btn-submit__label").textContent =
      loading ? "Signing in…" : "Sign in";
    submitBtn.querySelector(".btn-submit__spinner").hidden = !loading;
  }

  function getCookie(name) {
    var match = document.cookie.match("(^|;\\s*)(" + name + ")=([^;]*)");
    return match ? decodeURIComponent(match[3]) : null;
  }

  /* ========================================================================
     Password show/hide
     ======================================================================== */

  document.querySelectorAll(".password-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var input = document.getElementById(btn.getAttribute("data-target"));
      var isHidden = input.type === "password";
      input.type = isHidden ? "text" : "password";
      btn.setAttribute("aria-pressed", String(isHidden));
      btn.setAttribute("aria-label", isHidden ? "Hide password" : "Show password");
      btn.querySelector(".icon-eye").hidden = isHidden;
      btn.querySelector(".icon-eye-off").hidden = !isHidden;
    });
  });

  /* ========================================================================
     Forgot password — safe placeholder until the backend flow exists.
     Swap the body of this handler for a redirect to a real reset page or
     an API call once one is available; the rest of the page does not need
     to change.
     ======================================================================== */

  forgotPasswordLink.addEventListener("click", function (e) {
    e.preventDefault();
    clearMessages();
    showNotice("Password reset isn't available yet. Contact your administrator to reset your password.");
  });

  /* ========================================================================
     Validation
     ======================================================================== */

  function validate() {
    clearAllErrors();
    var ok = true;

    if (!fields.identifier.value.trim()) {
      setFieldError("identifier", "Enter your username or official email.");
      ok = false;
    }

    if (!fields.password.value) {
      setFieldError("password", "Enter your password.");
      ok = false;
    }

    return ok;
  }

  Object.keys(fields).forEach(function (name) {
    fields[name].addEventListener("input", function () { setFieldError(name, ""); });
  });

  /* ========================================================================
     Token / session persistence
     ------------------------------------------------------------------------
     Placeholder storage strategy: session-only by default, and also mirrored
     to localStorage when "Remember me" is checked so the session survives a
     browser restart. Swap this out to match the project's real auth design
     (e.g. httpOnly cookies set by the server) without touching the rest of
     this file — nothing else here depends on how tokens are persisted.
     Passwords are never persisted anywhere.
     ======================================================================== */

  function persistSession(tokens, rememberMe) {
    var store = rememberMe ? window.localStorage : window.sessionStorage;
    if (tokens.access) store.setItem("ncrb_drishti_access_token", tokens.access);
    if (tokens.refresh) store.setItem("ncrb_drishti_refresh_token", tokens.refresh);
  }

  /* ========================================================================
     Response handling
     ------------------------------------------------------------------------
     Backend response shape isn't finalized. This reads defensively: it looks
     for tokens under a few likely keys and checks account status under
     `user.status` (or a top-level `status`) before treating a 2xx response
     as a real login.
     ======================================================================== */

  var STATUS_MESSAGES = {
    PENDING: "Your account is still pending administrator approval. You cannot sign in until your account has been approved.",
    REJECTED: "Your account request was not approved. Please contact your administrator.",
    SUSPENDED: "Your account has been suspended. Please contact your administrator."
  };

  function extractStatus(data) {
    if (!data) return null;
    if (data.user && data.user.status) return String(data.user.status).toUpperCase();
    if (data.status) return String(data.status).toUpperCase();
    return null;
  }

  function extractTokens(data) {
    if (!data) return {};
    return {
      access: data.access || data.access_token || (data.tokens && data.tokens.access) || null,
      refresh: data.refresh || data.refresh_token || (data.tokens && data.tokens.refresh) || null
    };
  }

  function handleSuccess(data, rememberMe) {
    var status = extractStatus(data);

    if (status && status !== "ACTIVE" && status !== "APPROVED") {
      var message = STATUS_MESSAGES[status] ||
        "Your account cannot sign in right now. Please contact your administrator.";
      showAlert(message);
      return;
    }

    var tokens = extractTokens(data);
    if (tokens.access || tokens.refresh) {
      persistSession(tokens, rememberMe);
    }

    // Hand off to the app once the backend confirms an approved/active
    // session. Replace with the project's actual post-login route.
    window.location.assign("/dashboard/");
  }

  function handleFailure(status, data) {
    var accountStatus = extractStatus(data);
    if (accountStatus && STATUS_MESSAGES[accountStatus]) {
      showAlert(STATUS_MESSAGES[accountStatus]);
      return;
    }

    if (status === 400 || status === 401) {
      showAlert("Incorrect username/email or password. Please try again.");
      return;
    }

    if (status === 403) {
      showAlert("You are not permitted to sign in. Please contact your administrator.");
      return;
    }

    if (status >= 500) {
      showAlert("The server could not process your request. Please try again shortly.");
      return;
    }

    showAlert("Unable to sign in. Please try again.");
  }

  /* ========================================================================
     Submit
     ======================================================================== */

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (isSubmitting) return;

    clearMessages();
    if (!validate()) {
      var firstInvalid = form.querySelector('[aria-invalid="true"]');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    var rememberMe = document.getElementById("remember_me").checked;
    var payload = {
      identifier: fields.identifier.value.trim(),
      password: fields.password.value
    };

    setLoading(true);

    fetch(LOGIN_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken") || ""
      },
      credentials: "same-origin",
      body: JSON.stringify(payload)
    })
      .then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (data) {
          return { status: response.status, data: data };
        });
      })
      .then(function (result) {
        setLoading(false);
        if (result.status >= 200 && result.status < 300) {
          handleSuccess(result.data, rememberMe);
        } else {
          handleFailure(result.status, result.data);
        }
      })
      .catch(function () {
        setLoading(false);
        showAlert("Network error. Check your connection and try again.");
      });
  });
})();