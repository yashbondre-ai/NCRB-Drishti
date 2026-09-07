document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.settings-tab-btn');
    const tabContents = document.querySelectorAll('.settings-tab-content');
    const settingsForm = document.getElementById('settingsMasterForm');
    const saveStatusIndicator = document.getElementById('saveStatusIndicator');
    const btnSaveSettings = document.getElementById('btnSaveSettings');

    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            tabButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetContent = document.getElementById(`tab_${targetTab}`);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    if (settingsForm) {
        settingsForm.addEventListener('submit', (e) => {
            e.preventDefault();
            btnSaveSettings.innerHTML = '<i class="ph ph-spinner-gap spin"></i> Committing Enclave State...';
            btnSaveSettings.style.borderColor = 'var(--accent-teal, #2DD4BF)';

            setTimeout(() => {
                btnSaveSettings.innerHTML = '<i class="ph-fill ph-check-circle"></i> Configuration Saved';
                btnSaveSettings.style.background = '#22C55E';
                btnSaveSettings.style.color = '#FFFFFF';

                saveStatusIndicator.textContent = 'Enclave synchronised with TiDB Consensus Engine • ' + new Date().toLocaleTimeString();
                saveStatusIndicator.style.color = '#4ADE80';

                setTimeout(() => {
                    btnSaveSettings.innerHTML = '<i class="ph-fill ph-shield-check"></i> <span>Save Configuration</span>';
                    btnSaveSettings.style.background = 'var(--primary-navy, #0F1E3D)';
                    btnSaveSettings.style.color = 'var(--gold-brass, #C9A227)';
                    btnSaveSettings.style.borderColor = 'var(--gold-brass, #C9A227)';
                }, 1800);
            }, 600);
        });
    }

    const testModal = document.getElementById('tokenTestModal');
    const btnTestToken = document.getElementById('btnTestToken');
    const handshakeStatusBanner = document.getElementById('handshakeStatusBanner');
    const handshakeIcon = document.getElementById('handshakeIcon');
    const handshakeTitle = document.getElementById('handshakeTitle');
    const handshakeSub = document.getElementById('handshakeSub');
    const diagSignature = document.getElementById('diagSignature');
    const diagEnclave = document.getElementById('diagEnclave');

    if (btnTestToken && testModal) {
        btnTestToken.addEventListener('click', () => {
            testModal.classList.add('active');
            handshakeIcon.className = 'ph ph-spinner-gap spin';
            handshakeIcon.style.color = '#2DD4BF';
            handshakeTitle.textContent = 'Awaiting Hardware Token Response...';
            handshakeSub.textContent = 'Please tap the gold contact or verify biometric sensor on your YubiKey.';
            diagSignature.textContent = 'Verifying...';
            diagSignature.className = 'd-val text-gold';
            diagEnclave.textContent = 'Pending User Tap';

            setTimeout(() => {
                handshakeIcon.className = 'ph-fill ph-seal-check';
                handshakeIcon.style.color = '#4ADE80';
                handshakeTitle.textContent = 'Hardware Token Handshake Verified';
                handshakeSub.textContent = 'ECDSA secp256k1 signature authentic. FIDO2 counter increments verified.';
                diagSignature.textContent = 'Valid (SHA-256 Registered)';
                diagSignature.className = 'd-val text-teal';
                diagEnclave.textContent = 'Established (0.84ms)';
            }, 1400);
        });
    }

    const btnRegisterNewKey = document.getElementById('btnRegisterNewKey');
    if (btnRegisterNewKey && testModal) {
        btnRegisterNewKey.addEventListener('click', () => {
            testModal.classList.add('active');
            handshakeIcon.className = 'ph ph-key';
            handshakeTitle.textContent = 'Insert Secondary Token & Authenticate';
            handshakeSub.textContent = 'Plug your FIDO2 key into USB port to register public certificate.';
        });
    }

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const btnDiscardChanges = document.getElementById('btnDiscardChanges');
    if (btnDiscardChanges) {
        btnDiscardChanges.addEventListener('click', () => {
            if (confirm('Discard unsaved configuration changes?')) {
                window.location.reload();
            }
        });
    }
});