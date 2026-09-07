document.addEventListener('DOMContentLoaded', () => {
    const chatInputForm = document.getElementById('chatInputForm');
    const chatInputText = document.getElementById('chatInputText');
    const chatMessagesScroll = document.getElementById('chatMessagesScroll');
    const promptChips = document.querySelectorAll('.prompt-chip');
    const btnClearChat = document.getElementById('btnClearChat');
    const aiCaseSelector = document.getElementById('aiCaseSelector');

    function scrollToBottom() {
        if (chatMessagesScroll) {
            chatMessagesScroll.scrollTop = chatMessagesScroll.scrollHeight;
        }
    }

    function appendUserMessage(text) {
        const userBubble = document.createElement('div');
        userBubble.className = 'chat-bubble bubble-user';
        userBubble.innerHTML = `
            <div class="bubble-header">
                <span class="bubble-sender"><i class="ph-fill ph-user"></i> INVESTIGATION OFFICER</span>
                <span class="bubble-timestamp">Just Now</span>
            </div>
            <div class="bubble-body">
                <p>${text}</p>
            </div>
        `;
        chatMessagesScroll.appendChild(userBubble);
        scrollToBottom();
    }

    function appendAssistantResponse(htmlContent) {
        const assistantBubble = document.createElement('div');
        assistantBubble.className = 'chat-bubble bubble-assistant';
        assistantBubble.innerHTML = `
            <div class="bubble-header">
                <span class="bubble-sender"><i class="ph-fill ph-shield-check text-teal"></i> DRISHTI FORENSIC COPILOT</span>
                <span class="bubble-timestamp">Just Now</span>
            </div>
            <div class="bubble-body">
                ${htmlContent}
            </div>
        `;
        chatMessagesScroll.appendChild(assistantBubble);
        scrollToBottom();
    }

    function generateReasoningResponse(query) {
        const q = query.toLowerCase();

        if (q.includes('bns') || q.includes('section') || q.includes('statutory')) {
            return `
                <p>Based on the verified narrative extracted from <strong>FIR_MH26_0124.pdf</strong> and corroborated server intrusion logs, the following statutory provisions are strictly applicable:</p>
                <div class="legal-pill-cluster">
                    <span class="legal-pill pill-bns">BNS Sec 308(2) - Extortion</span>
                    <span class="legal-pill pill-it">IT Act Sec 66D - Cheating by Personation</span>
                    <span class="legal-pill pill-it">IT Act Sec 43 - Data Extraction</span>
                    <span class="legal-pill pill-bnss">BNSS Sec 173 - Cognizable Regular</span>
                </div>
                <table class="findings-table">
                    <thead>
                        <tr>
                            <th>Statutory Charge</th>
                            <th>Cognizable</th>
                            <th>Bail Matrix</th>
                            <th>Quantum of Punishment</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><strong>BNS Sec 308(2)</strong></td>
                            <td>Cognizable</td>
                            <td>Non-Bailable</td>
                            <td>Rigorous Imprisonment up to 7 Years</td>
                        </tr>
                        <tr>
                            <td><strong>IT Act Sec 66D</strong></td>
                            <td>Cognizable</td>
                            <td>Bailable</td>
                            <td>Imprisonment up to 3 Years + INR 1 Lakh Fine</td>
                        </tr>
                    </tbody>
                </table>
                <p><strong>Evidentiary Alignment:</strong> Both charges are sustained by memory extraction hash <code>7d86...9773</code> and the extortion communications ledger committed to TiDB Block #89104.</p>
            `;
        }

        if (q.includes('contradict') || q.includes('statement') || q.includes('cctv')) {
            return `
                <p><strong>Cross-Evidence Timeline Audit Executed:</strong> A chronometric contradiction was flagged between the suspect interrogation statement and digital forensic records:</p>
                <table class="findings-table">
                    <thead>
                        <tr>
                            <th>Evidence Source</th>
                            <th>Documented Event & Time</th>
                            <th>Audit Verification</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Suspect Deposition</td>
                            <td>Claims he vacated server premises at <strong>17:00 IST</strong></td>
                            <td>Uncorroborated statement</td>
                        </tr>
                        <tr>
                            <td>CCTV_ServerRoom_Access.mp4</td>
                            <td>Physical exit recorded at <strong>17:42:15 IST</strong></td>
                            <td><span class="text-teal font-mono">Matched SHA-256</span></td>
                        </tr>
                        <tr>
                            <td>RAM Dump Access Log</td>
                            <td>Admin binary exfiltration initiated at <strong>17:38:02 IST</strong></td>
                            <td><span class="text-gold font-mono">Forensic Signature Match</span></td>
                        </tr>
                    </tbody>
                </table>
                <p><span class="text-danger font-weight-bold">Adverse Inference:</span> The suspect was physically present inside the enclosure during the precise 4-minute window when corporate binaries were exfiltrated.</p>
            `;
        }

        if (q.includes('charge sheet') || q.includes('193') || q.includes('bnss')) {
            return `
                <p><strong>Section 193 BNSS Final Report (Charge Sheet) Draft Summary:</strong></p>
                <p><em>"Upon conclusion of statutory investigation under Section 173 BNSS in CR-2026-MH01, prima facie evidence proves that accused Sandeep K. Verma gained unauthorized administrative penetration into the complainant's proprietary data vault, extracted source binaries, and subsequently communicated extortion demands."</em></p>
                <p><strong>List of Cryptographic Productions for Trial:</strong></p>
                <ol style="margin-left: 16px; margin-bottom: 8px; font-size: 0.72rem; color: var(--text-secondary);">
                    <li>FIR_MH26_0124.pdf (Certified under Section 173 BNSS)</li>
                    <li>CCTV_ServerRoom_Access.mp4 (Sealed under Section 63/65B BSA)</li>
                    <li>Forensic_MemoryDump_Analysis.raw (Bit-level duplicate validated by DFSL)</li>
                </ol>
                <p>Ready to synthesize and export direct Section 193 Docket for Sessions Court submission.</p>
            `;
        }

        return `
            <p>Analysis complete for query: <em>"${query}"</em>.</p>
            <p>All cited digital assets in <strong>CR-2026-MH01</strong> have maintained unbroken Chain of Custody compliance under Section 63 of Bharatiya Sakshya Adhiniyam, 2023. Bitstream hashes match the active TiDB immutable vault.</p>
        `;
    }

    if (chatInputForm && chatInputText) {
        chatInputForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const text = chatInputText.value.trim();
            if (!text) return;

            appendUserMessage(text);
            chatInputText.value = '';

            setTimeout(() => {
                const responseHtml = generateReasoningResponse(text);
                appendAssistantResponse(responseHtml);
            }, 500);
        });

        chatInputText.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatInputForm.dispatchEvent(new Event('submit'));
            }
        });
    }

    promptChips.forEach(chip => {
        chip.addEventListener('click', () => {
            const promptText = chip.getAttribute('data-prompt');
            if (promptText) {
                appendUserMessage(promptText);
                setTimeout(() => {
                    const responseHtml = generateReasoningResponse(promptText);
                    appendAssistantResponse(responseHtml);
                }, 500);
            }
        });
    });

    if (btnClearChat && chatMessagesScroll) {
        btnClearChat.addEventListener('click', () => {
            chatMessagesScroll.innerHTML = `
                <div class="chat-bubble bubble-assistant">
                    <div class="bubble-header">
                        <span class="bubble-sender"><i class="ph-fill ph-shield-check text-teal"></i> DRISHTI FORENSIC COPILOT</span>
                        <span class="bubble-timestamp">Just Now</span>
                    </div>
                    <div class="bubble-body">
                        <p>Forensic context reset. Ready to analyze statutory sections, detect timeline contradictions, or synthesize court dockets.</p>
                    </div>
                </div>
            `;
        });
    }

    if (aiCaseSelector) {
        aiCaseSelector.addEventListener('change', (e) => {
            const val = e.target.value;
            const summaryBox = document.getElementById('contextDocketSummary');
            if (!summaryBox) return;

            if (val === 'CR-2026-MH04') {
                summaryBox.innerHTML = `
                    <div class="summary-line"><span class="s-label">Classification:</span><span class="s-val text-gold">Digital Forgery & Land Fraud</span></div>
                    <div class="summary-line"><span class="s-label">Lead IO:</span><span class="s-val">Insp. Amit Verma</span></div>
                    <div class="summary-line"><span class="s-label">Vaulted Evidence:</span><span class="s-val font-mono text-teal">12 Items (SHA-256 Sealed)</span></div>
                    <div class="summary-line"><span class="s-label">Jurisdiction:</span><span class="s-val">Sessions Court, Bhandara</span></div>
                `;
            } else if (val === 'CR-2026-MH09') {
                summaryBox.innerHTML = `
                    <div class="summary-line"><span class="s-label">Classification:</span><span class="s-val text-gold">Critical Infra Network Breach</span></div>
                    <div class="summary-line"><span class="s-label">Lead IO:</span><span class="s-val">Neha Patil (Cyber Cell)</span></div>
                    <div class="summary-line"><span class="s-label">Vaulted Evidence:</span><span class="s-val font-mono text-teal">18 Items (SHA-256 Sealed)</span></div>
                    <div class="summary-line"><span class="s-label">Jurisdiction:</span><span class="s-val">Sessions Court, Nagpur</span></div>
                `;
            } else {
                summaryBox.innerHTML = `
                    <div class="summary-line"><span class="s-label">Classification:</span><span class="s-val text-gold">Cyber Extortion & Espionage</span></div>
                    <div class="summary-line"><span class="s-label">Lead IO:</span><span class="s-val">Insp. Rahul Sharma</span></div>
                    <div class="summary-line"><span class="s-label">Vaulted Evidence:</span><span class="s-val font-mono text-teal">6 Items (SHA-256 Sealed)</span></div>
                    <div class="summary-line"><span class="s-label">Jurisdiction:</span><span class="s-val">Sessions Court, Bhandara</span></div>
                `;
            }
        });
    }
});