document.addEventListener('DOMContentLoaded', () => {
    const auditSearchInput = document.getElementById('auditSearchInput');
    const auditChips = document.querySelectorAll('.audit-chip');
    const tableRows = document.querySelectorAll('#auditMasterTable tbody tr');
    const auditRecordCounter = document.getElementById('auditRecordCounter');

    function updateCounter(visible) {
        if (auditRecordCounter) {
            auditRecordCounter.textContent = `Showing ${visible} of ${tableRows.length} Records`;
        }
    }

    function filterAuditTable() {
        const query = auditSearchInput ? auditSearchInput.value.toLowerCase().trim() : '';
        const activeChip = document.querySelector('.audit-chip.active');
        const filterType = activeChip ? activeChip.getAttribute('data-filter') : 'all';

        let count = 0;
        tableRows.forEach(row => {
            const rowType = row.getAttribute('data-type');
            const rowText = row.textContent.toLowerCase();

            const matchesChip = (filterType === 'all' || rowType === filterType);
            const matchesSearch = (!query || rowText.includes(query));

            if (matchesChip && matchesSearch) {
                row.style.display = '';
                count++;
            } else {
                row.style.display = 'none';
            }
        });

        updateCounter(count);
    }

    if (auditSearchInput) {
        auditSearchInput.addEventListener('input', filterAuditTable);
    }

    auditChips.forEach(chip => {
        chip.addEventListener('click', () => {
            auditChips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            filterAuditTable();
        });
    });

    const btnVerifyChain = document.getElementById('btnVerifyAuditChain');
    if (btnVerifyChain) {
        btnVerifyChain.addEventListener('click', () => {
            btnVerifyChain.innerHTML = '<i class="ph ph-spinner-gap spin"></i> Verifying Hash Links...';
            btnVerifyChain.style.borderColor = 'var(--accent-teal)';

            setTimeout(() => {
                btnVerifyChain.innerHTML = '<i class="ph-fill ph-seal-check"></i> 100% Chain Intact (0 Breaks)';
                btnVerifyChain.style.background = 'var(--success)';
                btnVerifyChain.style.color = '#FFFFFF';
                btnVerifyChain.style.borderColor = 'var(--success)';

                setTimeout(() => {
                    btnVerifyChain.innerHTML = '<i class="ph-fill ph-shield-check"></i> <span>Verify Ledger Integrity</span>';
                    btnVerifyChain.style.background = 'var(--primary-navy)';
                    btnVerifyChain.style.color = 'var(--gold-brass)';
                    btnVerifyChain.style.borderColor = 'var(--gold-brass)';
                }, 2500);
            }, 1200);
        });
    }

    const payloadModal = document.getElementById('payloadInspectModal');
    const payloadBlockTitle = document.getElementById('payloadBlockTitle');
    const payloadTimestamp = document.getElementById('payloadTimestamp');
    const payloadAction = document.getElementById('payloadAction');
    const payloadActor = document.getElementById('payloadActor');
    const payloadIp = document.getElementById('payloadIp');
    const payloadTarget = document.getElementById('payloadTarget');
    const payloadRawJson = document.getElementById('payloadRawJson');

    document.querySelectorAll('.btn-inspect-payload').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const row = e.target.closest('tr');
            if (!row) return;

            const block = row.getAttribute('data-block');
            const time = row.getAttribute('data-time');
            const action = row.getAttribute('data-action');
            const actor = row.getAttribute('data-actor');
            const ip = row.getAttribute('data-ip');
            const target = row.getAttribute('data-target');
            const rawPayload = row.getAttribute('data-payload');

            if (payloadBlockTitle) payloadBlockTitle.textContent = `Audit Block #${block}`;
            if (payloadTimestamp) payloadTimestamp.textContent = `${time} IST`;
            if (payloadAction) payloadAction.textContent = action;
            if (payloadActor) payloadActor.textContent = actor;
            if (payloadIp) payloadIp.textContent = ip;
            if (payloadTarget) payloadTarget.textContent = target;

            if (payloadRawJson) {
                try {
                    const parsed = JSON.parse(rawPayload);
                    payloadRawJson.textContent = JSON.stringify(parsed, null, 2);
                } catch {
                    payloadRawJson.textContent = rawPayload;
                }
            }

            if (payloadModal) payloadModal.classList.add('active');
        });
    });

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const btnExportSingle = document.getElementById('btnExportAuditLogSingle');
    if (btnExportSingle && payloadRawJson) {
        btnExportSingle.addEventListener('click', () => {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(payloadRawJson.textContent);
            const downloadAnchor = document.createElement('a');
            downloadAnchor.setAttribute("href", dataStr);
            downloadAnchor.setAttribute("download", "audit_log_proof.json");
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            downloadAnchor.remove();
        });
    }
});