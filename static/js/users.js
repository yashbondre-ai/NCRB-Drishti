document.addEventListener('DOMContentLoaded', () => {
    const roleChips = document.querySelectorAll('.role-chip');
    const officerCards = document.querySelectorAll('.officer-credential-card');
    const officerSearchInput = document.getElementById('officerSearchInput');
    const officerCountLabel = document.getElementById('officerCountLabel');

    const activeRoleTitle = document.getElementById('activeRoleTitle');
    const activeRoleResp = document.getElementById('activeRoleResp');

    const permUserConfig = document.getElementById('permUserConfig');
    const permDeptCase = document.getElementById('permDeptCase');
    const permEvidenceUpload = document.getElementById('permEvidenceUpload');
    const permLegalDocs = document.getElementById('permLegalDocs');
    const permReviewApprove = document.getElementById('permReviewApprove');
    const permAuditLogs = document.getElementById('permAuditLogs');
    const permViewOnly = document.getElementById('permViewOnly');

    const rolesMap = {
        super_admin: {
            title: "Super Admin",
            resp: "System-wide administration",
            perms: { userConfig: true, deptCase: true, evidence: true, legal: true, review: true, audit: true, view: true }
        },
        dept_admin: {
            title: "Department Admin",
            resp: "Manage users/documents within a department",
            perms: { userConfig: false, deptCase: true, evidence: true, legal: false, review: true, audit: true, view: true }
        },
        investigation_officer: {
            title: "Investigation Officer",
            resp: "Handle investigation and case documents",
            perms: { userConfig: false, deptCase: false, evidence: true, legal: false, review: false, audit: false, view: true }
        },
        case_officer: {
            title: "Case Officer / Case Manager",
            resp: "Manage a specific assigned case",
            perms: { userConfig: false, deptCase: false, evidence: true, legal: false, review: false, audit: false, view: true }
        },
        legal_officer: {
            title: "Legal Officer",
            resp: "Handle legal/court-related documents",
            perms: { userConfig: false, deptCase: false, evidence: false, legal: true, review: false, audit: false, view: true }
        },
        forensic_officer: {
            title: "Evidence/Forensic Officer",
            resp: "Manage evidence and forensic records",
            perms: { userConfig: false, deptCase: false, evidence: true, legal: false, review: true, audit: false, view: true }
        },
        reviewer: {
            title: "Reviewer / Approver",
            resp: "Verify documents before finalization",
            perms: { userConfig: false, deptCase: false, evidence: false, legal: false, review: true, audit: false, view: true }
        },
        auditor: {
            title: "Auditor",
            resp: "Monitor system activities (Read-only)",
            perms: { userConfig: false, deptCase: false, evidence: false, legal: false, review: false, audit: true, view: true }
        },
        viewer: {
            title: "Viewer",
            resp: "Read-only stakeholder (Explicit authorization)",
            perms: { userConfig: false, deptCase: false, evidence: false, legal: false, review: false, audit: false, view: true }
        }
    };

    function setCheckState(elem, isEnabled) {
        if (!elem) return;
        if (isEnabled) {
            elem.className = "permission-check enabled";
            elem.innerHTML = '<i class="ph-fill ph-check"></i>';
        } else {
            elem.className = "permission-check disabled";
            elem.innerHTML = '<i class="ph-fill ph-x"></i>';
        }
    }

    function updateMatrix(roleKey) {
        const roleData = rolesMap[roleKey] || rolesMap['super_admin'];
        if (activeRoleTitle) activeRoleTitle.textContent = roleData.title;
        if (activeRoleResp) activeRoleResp.textContent = roleData.resp;

        setCheckState(permUserConfig, roleData.perms.userConfig);
        setCheckState(permDeptCase, roleData.perms.deptCase);
        setCheckState(permEvidenceUpload, roleData.perms.evidence);
        setCheckState(permLegalDocs, roleData.perms.legal);
        setCheckState(permReviewApprove, roleData.perms.review);
        setCheckState(permAuditLogs, roleData.perms.audit);
        setCheckState(permViewOnly, roleData.perms.view);
    }

    function filterDirectory() {
        const query = officerSearchInput ? officerSearchInput.value.toLowerCase().trim() : '';
        const activeChip = document.querySelector('.role-chip.active');
        const selectedRole = activeChip ? activeChip.getAttribute('data-role') : 'all';

        let count = 0;
        officerCards.forEach(card => {
            const cardRole = card.getAttribute('data-role');
            const cardText = card.textContent.toLowerCase();

            const matchesRole = (selectedRole === 'all' || cardRole === selectedRole);
            const matchesSearch = (!query || cardText.includes(query));

            if (matchesRole && matchesSearch) {
                card.style.display = 'flex';
                count++;
            } else {
                card.style.display = 'none';
            }
        });

        if (officerCountLabel) {
            officerCountLabel.textContent = `Showing ${count} Officers`;
        }
    }

    roleChips.forEach(chip => {
        chip.addEventListener('click', () => {
            roleChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            const role = chip.getAttribute('data-role');
            if (role !== 'all') {
                updateMatrix(role);
            } else {
                updateMatrix('super_admin');
            }
            filterDirectory();
        });
    });

    if (officerSearchInput) {
        officerSearchInput.addEventListener('input', filterDirectory);
    }

    const tokenModal = document.getElementById('tokenInspectModal');
    const tokenModalOfficerName = document.getElementById('tokenModalOfficerName');
    const tokenModalBadgeNumber = document.getElementById('tokenModalBadgeNumber');
    const tokenModelVal = document.getElementById('tokenModelVal');
    const tokenRoleVal = document.getElementById('tokenRoleVal');
    const tokenDeptVal = document.getElementById('tokenDeptVal');
    const tokenFingerprintVal = document.getElementById('tokenFingerprintVal');

    document.querySelectorAll('.btn-inspect-key').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.officer-credential-card');
            if (!card) return;

            const name = card.getAttribute('data-name');
            const id = card.getAttribute('data-id');
            const role = card.getAttribute('data-role');
            const token = card.getAttribute('data-token');
            const fp = card.getAttribute('data-fp');
            const dept = card.getAttribute('data-dept');

            if (tokenModalOfficerName) tokenModalOfficerName.textContent = name;
            if (tokenModalBadgeNumber) tokenModalBadgeNumber.textContent = `Badge ID: ${id}`;
            if (tokenModelVal) tokenModelVal.textContent = token;
            if (tokenRoleVal) tokenRoleVal.textContent = (rolesMap[role] ? rolesMap[role].title.toUpperCase() : role.toUpperCase());
            if (tokenDeptVal) tokenDeptVal.textContent = dept;
            if (tokenFingerprintVal) tokenFingerprintVal.textContent = fp;

            if (tokenModal) tokenModal.classList.add('active');
        });
    });

    const provisionModal = document.getElementById('provisionKeyModal');
    const btnOpenProvision = document.getElementById('btnOpenProvisionModal');
    if (btnOpenProvision && provisionModal) {
        btnOpenProvision.addEventListener('click', () => {
            provisionModal.classList.add('active');
        });
    }

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const provisionForm = document.getElementById('provisionTokenForm');
    if (provisionForm) {
        provisionForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('btnSaveCredential');
            if (submitBtn) {
                submitBtn.innerHTML = '<i class="ph-fill ph-seal-check"></i> Role Bound to Hardware CA';
                submitBtn.style.background = 'var(--success)';
            }
            setTimeout(() => {
                if (provisionModal) provisionModal.classList.remove('active');
                provisionForm.reset();
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="ph ph-shield-check"></i> Bind Role & Issue Certificate';
                    submitBtn.style.background = 'var(--primary-navy)';
                }
            }, 1200);
        });
    }

    updateMatrix('super_admin');
});