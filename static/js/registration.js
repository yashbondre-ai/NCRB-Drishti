(function () {
  "use strict";

  /* ========================================================================
     Role responsibility hints (display-only; selecting a role never grants
     permissions — every new account is created with status = PENDING).
     ======================================================================== */
  var ROLE_HINTS = {
    SUPER_ADMIN: "System-wide administration: manage users, roles, departments, permissions and configuration; view all audit logs.",
    DEPARTMENT_ADMIN: "Manage users and documents within a department; add department users, create cases, manage documents, view department audit logs.",
    INVESTIGATION_OFFICER: "Create and update cases, upload documents, view authorized documents, create investigation records.",
    CASE_OFFICER: "Manage an assigned case: view case documents, upload or update permitted documents, manage case workflow.",
    LEGAL_OFFICER: "View assigned cases, upload legal documents, add legal records, access court filings and judgments.",
    EVIDENCE_FORENSIC_OFFICER: "Upload evidence and forensic documents, update evidence metadata, verify integrity.",
    REVIEWER_APPROVER: "Review documents, approve or reject them, verify document integrity before finalization.",
    AUDITOR: "Read-only access to audit logs, document history and access history.",
    VIEWER: "Read-only access to documents and cases explicitly authorized for you."
  };

  var form = document.getElementById("registrationForm");
  var registrationView = document.getElementById("registrationView");
  var pendingView = document.getElementById("pendingView");
  var formAlert = document.getElementById("formAlert");
  var submitBtn = document.getElementById("submitBtn");
  var roleSelect = document.getElementById("role");
  var roleHint = document.getElementById("roleHint");

  var fields = {
    full_name: document.getElementById("full_name"),
    username: document.getElementById("username"),
    email: document.getElementById("email"),
    mobile_number: document.getElementById("mobile_number"),
    role: roleSelect,
    password: document.getElementById("password"),
    confirm_password: document.getElementById("confirm_password"),
    usage_policy: document.getElementById("usage_policy")
  };

  /* ========================================================================
     Helpers
     ======================================================================== */

  function getCookie(name) {
    var match = document.cookie.match("(^|;\\s*)(" + name + ")=([^;]*)");
    return match ? decodeURIComponent(match[3]) : null;
  }

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

  function showFormAlert(message) {
    formAlert.textContent = message;
    formAlert.hidden = !message;
  }

  // Splits "Rahul Kumar Sharma" -> { first_name: "Rahul", last_name: "Kumar Sharma" }.
  // A single-word name has no last name; the caller decides how to treat that.
  function splitFullName(fullName) {
    var parts = fullName.trim().replace(/\s+/g, " ").split(" ");
    var first = parts.shift() || "";
    var last = parts.join(" ");
    return { first_name: first, last_name: last };
  }

  function setLoading(isLoading) {
    submitBtn.disabled = isLoading;
    submitBtn.querySelector(".btn-submit__label").textContent =
      isLoading ? "Submitting request…" : "Submit request";
    submitBtn.querySelector(".btn-submit__spinner").hidden = !isLoading;
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
     Role hint
     ======================================================================== */

  roleSelect.addEventListener("change", function () {
    roleHint.textContent = ROLE_HINTS[roleSelect.value] || "";
  });

  /* ========================================================================
     Validation
     ======================================================================== */

  var USERNAME_RE = /^[A-Za-z0-9._-]{4,}$/;
  var EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  var MOBILE_RE = /^\d{10}$/;

  function validate() {
    clearAllErrors();
    var ok = true;

    var fullName = fields.full_name.value.trim();
    if (!fullName) {
      setFieldError("full_name", "Full name is required.");
      ok = false;
    } else if (fullName.split(/\s+/).length < 2) {
      setFieldError("full_name", "Enter your first and last name.");
      ok = false;
    }

    var username = fields.username.value.trim();
    if (!username) {
      setFieldError("username", "Username is required.");
      ok = false;
    } else if (!USERNAME_RE.test(username)) {
      setFieldError("username", "At least 4 characters. Letters, numbers, dots, hyphens and underscores only — no spaces.");
      ok = false;
    }

    var email = fields.email.value.trim();
    if (!email) {
      setFieldError("email", "Official email is required.");
      ok = false;
    } else if (!EMAIL_RE.test(email)) {
      setFieldError("email", "Enter a valid email address.");
      ok = false;
    }

    var mobile = fields.mobile_number.value.trim();
    if (!mobile) {
      setFieldError("mobile_number", "Mobile number is required.");
      ok = false;
    } else if (!MOBILE_RE.test(mobile)) {
      setFieldError("mobile_number", "Enter exactly 10 digits, numbers only.");
      ok = false;
    }

    if (!fields.role.value) {
      setFieldError("role", "Select a role.");
      ok = false;
    }

    var password = fields.password.value;
    if (!password) {
      setFieldError("password", "Password is required.");
      ok = false;
    } else if (password.length < 8) {
      setFieldError("password", "Password must be at least 8 characters.");
      ok = false;
    }

    var confirmPassword = fields.confirm_password.value;
    if (!confirmPassword) {
      setFieldError("confirm_password", "Confirm your password.");
      ok = false;
    } else if (password && confirmPassword !== password) {
      setFieldError("confirm_password", "Passwords do not match.");
      ok = false;
    }

    if (!fields.usage_policy.checked) {
      setFieldError("usage_policy", "You must accept the usage policy to submit a request.");
      ok = false;
    }

    return ok;
  }

  // Clear a field's error as soon as the user edits it.
  Object.keys(fields).forEach(function (name) {
    var el = fields[name];
    if (!el) return;
    var evt = el.type === "checkbox" || el.tagName === "SELECT" ? "change" : "input";
    el.addEventListener(evt, function () { setFieldError(name, ""); });
  });

  /* ========================================================================
     Submit
     ======================================================================== */

  function buildPayload() {
    var name = splitFullName(fields.full_name.value);
    return {
      first_name: name.first_name,
      last_name: name.last_name,
      username: fields.username.value.trim(),
      email: fields.email.value.trim().toLowerCase(),
      mobile: fields.mobile_number.value.trim(),
      password: fields.password.value,
      confirm_password: fields.confirm_password.value,
      role: fields.role.value
    };
  }

  // Maps a Django/DRF error response onto the matching field. Falls back to
  // the general alert area when an error can't be tied to one input.
  function applyServerErrors(status, data) {
    var handled = false;
    var fieldErrorMap = {
      username: "username",
      email: "email",
      mobile: "mobile_number",
      role: "role",
      password: "password",
      confirm_password: "confirm_password",
      first_name: "full_name",
      last_name: "full_name",
      non_field_errors: null
    };

    if (data && typeof data === "object") {
      Object.keys(data).forEach(function (key) {
        var targetField = fieldErrorMap[key];
        var rawMessage = data[key];
        var message = Array.isArray(rawMessage) ? rawMessage.join(" ") : String(rawMessage);
        if (targetField && fields[targetField]) {
          setFieldError(targetField, message);
          handled = true;
        }
      });
    }

    if (status === 409) {
      showFormAlert("An account with these details already exists. Check the username, email and mobile number.");
      handled = true;
    }

    if (!handled) {
      if (status === 400) {
        showFormAlert("Please correct the highlighted fields and try again.");
      } else if (status === 401 || status === 403) {
        showFormAlert("You are not permitted to perform this action.");
      } else if (status >= 500) {
        showFormAlert("The server could not process your request. Please try again shortly.");
      } else {
        showFormAlert("Something went wrong. Please try again.");
      }
    }
  }

  function showPendingView(username) {
    registrationView.hidden = true;
    pendingView.hidden = false;
    document.getElementById("pendingUsername").textContent = username || "—";
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    showFormAlert("");

    if (!validate()) {
      var firstInvalid = form.querySelector('[aria-invalid="true"]');
      if (firstInvalid) firstInvalid.focus();
      return;
    }

    setLoading(true);

    fetch(REGISTER_ENDPOINT, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken") || ""
      },
      credentials: "same-origin",
      body: JSON.stringify(buildPayload())
    })
      .then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (data) {
          return { status: response.status, data: data };
        });
      })
      .then(function (result) {
        setLoading(false);
        if (result.status >= 200 && result.status < 300) {
          form.reset();
          showPendingView(result.data && result.data.username);
        } else {
          applyServerErrors(result.status, result.data);
        }
      })
      .catch(function () {
        setLoading(false);
        showFormAlert("Network error. Check your connection and try again.");
      });
  });
})();