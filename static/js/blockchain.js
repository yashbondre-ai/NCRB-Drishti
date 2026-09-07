document.addEventListener('DOMContentLoaded', () => {
    const targetHashInput = document.getElementById('targetHashInput');
    const btnExecuteVerify = document.getElementById('btnExecuteVerify');
    const presetPills = document.querySelectorAll('.preset-pill');

    const certStampBox = document.getElementById('certStampBox');
    const certIcon = document.getElementById('certIcon');
    const certVerdict = document.getElementById('certVerdict');
    const certSubtext = document.getElementById('certSubtext');
    const resBlock = document.getElementById('resBlock');
    const resLatency = document.getElementById('resLatency');
    const resMerkle = document.getElementById('resMerkle');

    const VALID_HASH = "4f8a92b3c1048e91827419baedbc58129a01f8d9b2341256789abcdef0123456";
    const TAMPERED_HASH = "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e";

    presetPills.forEach(pill => {
        pill.addEventListener('click', () => {
            const presetType = pill.getAttribute('data-preset');
            if (presetType === 'valid') {
                targetHashInput.value = VALID_HASH;
            } else {
                targetHashInput.value = TAMPERED_HASH;
            }
            triggerVerification();
        });
    });

    function triggerVerification() {
        const enteredHash = targetHashInput.value.trim();
        if (!enteredHash) return;

        btnExecuteVerify.innerHTML = '<i class="ph ph-spinner-gap spin"></i> Verifying Across 3 Nodes...';
        btnExecuteVerify.style.borderColor = 'var(--accent-teal)';

        setTimeout(() => {
            if (enteredHash === TAMPERED_HASH || enteredHash.toLowerCase().includes('tamper')) {
                certStampBox.className = 'cert-stamp-box tampered';
                certIcon.className = 'ph-fill ph-warning-octagon';
                certVerdict.textContent = 'ALERT: ON-CHAIN HASH MISMATCH';
                certSubtext.textContent = 'Bitstream alteration quarantined. Consensus quorum rejected proof.';
                resBlock.textContent = 'REJECTED';
                resBlock.className = 'b-val font-mono text-danger';
                resLatency.textContent = '19.8 ms';
                resMerkle.textContent = 'FAIL (Root Mismatch)';
                resMerkle.className = 'b-val font-mono text-danger';
            } else {
                certStampBox.className = 'cert-stamp-box valid';
                certIcon.className = 'ph-fill ph-seal-check';
                certVerdict.textContent = 'ON-CHAIN VERIFIED: UNTAMPERED';
                certSubtext.textContent = 'Bit-level verification matches 3/3 Byzantine Consortium Nodes';
                resBlock.textContent = 'Block #89104';
                resBlock.className = 'b-val font-mono text-gold';
                resLatency.textContent = '14.2 ms';
                resMerkle.textContent = 'PASSED (Root #0x8f3b)';
                resMerkle.className = 'b-val font-mono text-success';
            }

            btnExecuteVerify.innerHTML = '<i class="ph-fill ph-shield-check"></i> <span>Verify On-Chain Integrity</span>';
            btnExecuteVerify.style.borderColor = 'var(--gold-brass)';
        }, 800);
    }

    if (btnExecuteVerify) {
        btnExecuteVerify.addEventListener('click', triggerVerification);
    }

    const certModal = document.getElementById('blockchainCertModal');
    const certFieldFile = document.getElementById('certFieldFile');
    const certFieldDocket = document.getElementById('certFieldDocket');
    const certFieldBlock = document.getElementById('certFieldBlock');
    const certFieldTime = document.getElementById('certFieldTime');
    const certFieldHash = document.getElementById('certFieldHash');

    const btnOpenCert = document.getElementById('btnOpenCertModal');
    if (btnOpenCert && certModal) {
        btnOpenCert.addEventListener('click', () => {
            if (certFieldFile) certFieldFile.textContent = "FIR_MH26_0124.pdf";
            if (certFieldDocket) certFieldDocket.textContent = "CR-2026-MH01";
            if (certFieldBlock) certFieldBlock.textContent = resBlock.textContent;
            if (certFieldTime) certFieldTime.textContent = "02 Aug 2026 10:30 IST";
            if (certFieldHash) certFieldHash.textContent = targetHashInput.value;
            certModal.classList.add('active');
        });
    }

    document.querySelectorAll('.btn-block-inspect').forEach(btn => {
        btn.addEventListener('click', () => {
            const block = btn.getAttribute('data-block');
            const file = btn.getAttribute('data-file');
            const docket = btn.getAttribute('data-docket');
            const time = btn.getAttribute('data-time');
            const tx = btn.getAttribute('data-tx');

            if (certFieldFile) certFieldFile.textContent = file;
            if (certFieldDocket) certFieldDocket.textContent = docket;
            if (certFieldBlock) certFieldBlock.textContent = `Block #${block}`;
            if (certFieldTime) certFieldTime.textContent = time;
            if (certFieldHash) certFieldHash.textContent = tx;

            if (certModal) certModal.classList.add('active');
        });
    });

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const printCertBtn = document.getElementById('btnPrintCert');
    if (printCertBtn) {
        printCertBtn.addEventListener('click', () => {
            window.print();
        });
    }
});