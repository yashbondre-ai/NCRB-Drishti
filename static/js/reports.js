document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('clearanceTrendChart');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        const months = ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'];
        const inflowData = [180, 220, 240, 210, 290, 260];
        const clearanceData = [140, 190, 210, 185, 250, 235];

        const padding = 35;
        const chartWidth = canvas.width - padding * 2;
        const chartHeight = canvas.height - padding * 2;
        const maxVal = 320;
        const barWidth = 14;
        const gap = chartWidth / months.length;

        ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = padding + (chartHeight / 4) * i;
            ctx.beginPath();
            ctx.moveTo(padding, y);
            ctx.lineTo(canvas.width - padding, y);
            ctx.stroke();

            ctx.fillStyle = '#64748B';
            ctx.font = '10px JetBrains Mono';
            ctx.fillText(Math.round(maxVal - (maxVal / 4) * i), 10, y + 3);
        }

        months.forEach((m, idx) => {
            const xCenter = padding + gap * idx + gap / 2;

            const hInflow = (inflowData[idx] / maxVal) * chartHeight;
            const yInflow = canvas.height - padding - hInflow;
            ctx.fillStyle = '#2563EB';
            ctx.beginPath();
            ctx.roundRect(xCenter - barWidth - 2, yInflow, barWidth, hInflow, [3, 3, 0, 0]);
            ctx.fill();

            const hClearance = (clearanceData[idx] / maxVal) * chartHeight;
            const yClearance = canvas.height - padding - hClearance;
            ctx.fillStyle = '#2DD4BF';
            ctx.beginPath();
            ctx.roundRect(xCenter + 2, yClearance, barWidth, hClearance, [3, 3, 0, 0]);
            ctx.fill();

            ctx.fillStyle = '#94A3B8';
            ctx.font = '11px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(m, xCenter, canvas.height - 12);
        });
    }

    const reportForm = document.getElementById('reportGeneratorForm');
    const btnCompile = document.getElementById('btnCompileReport');
    if (reportForm && btnCompile) {
        reportForm.addEventListener('submit', (e) => {
            e.preventDefault();
            btnCompile.innerHTML = '<i class="ph ph-spinner-gap spin"></i> Compiling Dossier...';
            btnCompile.style.borderColor = 'var(--accent-teal)';

            setTimeout(() => {
                btnCompile.innerHTML = '<i class="ph-fill ph-check-circle"></i> Dossier Exported';
                btnCompile.style.background = 'var(--accent-teal)';
                btnCompile.style.color = '#FFFFFF';

                setTimeout(() => {
                    btnCompile.innerHTML = '<i class="ph-fill ph-gear"></i> <span>Generate Dossier</span>';
                    btnCompile.style.background = 'var(--primary-navy)';
                    btnCompile.style.color = 'var(--gold-brass)';
                    btnCompile.style.borderColor = 'var(--gold-brass)';
                }, 2200);
            }, 1400);
        });
    }

    const catalogTabs = document.querySelectorAll('.catalog-tab');
    const publishedCards = document.querySelectorAll('.published-card');

    catalogTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            catalogTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            const target = tab.getAttribute('data-cat');

            publishedCards.forEach(card => {
                const cardCat = card.getAttribute('data-cat');
                if (target === 'all' || cardCat === target) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });

    const previewModal = document.getElementById('reportPreviewModal');
    const modalTitle = document.getElementById('modalReportTitle');
    const repSheetSubject = document.getElementById('repSheetSubject');

    document.querySelectorAll('.btn-preview-report').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const card = e.target.closest('.published-card');
            if (!card) return;

            const title = card.querySelector('.published-title').textContent;
            if (modalTitle) modalTitle.textContent = title;
            if (repSheetSubject) repSheetSubject.textContent = title;

            if (previewModal) previewModal.classList.add('active');
        });
    });

    document.querySelectorAll('[data-close]').forEach(btn => {
        btn.addEventListener('click', () => {
            const modalId = btn.getAttribute('data-close');
            const modal = document.getElementById(modalId);
            if (modal) modal.classList.remove('active');
        });
    });

    const printDossierBtn = document.getElementById('btnPrintReportDossier');
    if (printDossierBtn) {
        printDossierBtn.addEventListener('click', () => {
            window.print();
        });
    }
});