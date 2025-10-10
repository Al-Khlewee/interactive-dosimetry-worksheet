document.addEventListener('DOMContentLoaded', () => {
    // --- DATA TABLES from TRS-398 ---
    const k_Q_photon_data = {
        'NE 2571': { 0.50: 1.026, 0.52: 1.023, 0.54: 1.020, 0.56: 1.017, 0.58: 1.014, 0.60: 1.011, 0.62: 1.008, 0.64: 1.004, 0.66: 1.000, 0.68: 0.996, 0.70: 0.992, 0.72: 0.988, 0.74: 0.984, 0.76: 0.980, 0.78: 0.975, 0.80: 0.970, 0.82: 0.964, 0.84: 0.958 },
        'NE 2581': { 0.50: 1.025, 0.52: 1.022, 0.54: 1.019, 0.56: 1.016, 0.58: 1.013, 0.60: 1.010, 0.62: 1.007, 0.64: 1.003, 0.66: 1.000, 0.68: 0.996, 0.70: 0.992, 0.72: 0.988, 0.74: 0.984, 0.76: 0.980, 0.78: 0.975, 0.80: 0.970, 0.82: 0.965, 0.84: 0.959 },
        'NE 2611A': { 0.50: 1.028, 0.52: 1.025, 0.54: 1.022, 0.56: 1.019, 0.58: 1.016, 0.60: 1.013, 0.62: 1.009, 0.64: 1.005, 0.66: 1.000, 0.68: 0.996, 0.70: 0.991, 0.72: 0.987, 0.74: 0.982, 0.76: 0.977, 0.78: 0.972, 0.80: 0.966, 0.82: 0.960, 0.84: 0.954 },
        'FC65-G': { 0.50: 1.025, 0.52: 1.022, 0.54: 1.019, 0.56: 1.016, 0.58: 1.013, 0.60: 1.010, 0.62: 1.007, 0.64: 1.003, 0.66: 1.000, 0.68: 0.996, 0.70: 0.992, 0.72: 0.988, 0.74: 0.984, 0.76: 0.979, 0.78: 0.974, 0.80: 0.969, 0.82: 0.963, 0.84: 0.957 },
        'PTW 30001': { 0.50: 1.028, 0.52: 1.025, 0.54: 1.022, 0.56: 1.019, 0.58: 1.016, 0.60: 1.013, 0.62: 1.009, 0.64: 1.005, 0.66: 1.000, 0.68: 0.996, 0.70: 0.991, 0.72: 0.987, 0.74: 0.982, 0.76: 0.977, 0.78: 0.972, 0.80: 0.966, 0.82: 0.960, 0.84: 0.954 },
        'PTW 30004': { 0.50: 1.027, 0.52: 1.024, 0.54: 1.021, 0.56: 1.018, 0.58: 1.015, 0.60: 1.012, 0.62: 1.008, 0.64: 1.004, 0.66: 1.000, 0.68: 0.996, 0.70: 0.991, 0.72: 0.987, 0.74: 0.982, 0.76: 0.977, 0.78: 0.972, 0.80: 0.967, 0.82: 0.961, 0.84: 0.955 },
    };
    const k_Q_electron_data = {
        'NACP-02': { 1:0.925, 2:0.921, 3:0.917, 4:0.914, 5:0.910, 6:0.906, 7:0.903, 8:0.900, 9:0.897, 10:0.894, 12:0.890, 14:0.887, 16:0.885, 18:0.884, 20:0.883 },
        'Markus': { 1:0.941, 2:0.936, 3:0.932, 4:0.927, 5:0.922, 6:0.917, 7:0.913, 8:0.908, 9:0.904, 10:0.900, 12:0.895, 14:0.891, 16:0.888, 18:0.886, 20:0.885 },
        'Roos': { 1:0.928, 2:0.924, 3:0.920, 4:0.916, 5:0.912, 6:0.908, 7:0.905, 8:0.902, 9:0.899, 10:0.896, 12:0.892, 14:0.889, 16:0.887, 18:0.886, 20:0.885 },
        'PTW 34001': { 1:0.935, 2:0.930, 3:0.926, 4:0.922, 5:0.918, 6:0.914, 7:0.910, 8:0.906, 9:0.903, 10:0.900, 12:0.895, 14:0.892, 16:0.889, 18:0.887, 20:0.886 },
    };
    const ksCoefficients = {
        2.0: { a0: 1.198, a1: -0.875, a2: 0.677 }, 2.5: { a0: 1.706, a1: -2.063, a2: 1.357 }, 3.0: { a0: 2.337, a1: -3.636, a2: 2.299 }, 3.5: { a0: 3.091, a1: -5.600, a2: 3.509 }, 4.0: { a0: 3.968, a1: -7.955, a2: 4.987 }, 5.0: { a0: 6.081, a1: -13.52, a2: 8.439 }
    };

    // --- UTILITY FUNCTIONS ---
    const getNumericValue = id => parseFloat(document.getElementById(id).value) || 0;
    const setInputValue = (id, value) => { document.getElementById(id).value = value; };
    const getSelectedValue = id => document.getElementById(id).value;
    
    function interpolate(x, x0, y0, x1, y1) {
        if (x1 === x0) return y0;
        return y0 + (x - x0) * (y1 - y0) / (x1 - x0);
    }

    function lookupKq(quality, chamberModel, dataTable) {
        const chamberData = dataTable[chamberModel];
        if (!chamberData) return null;

        const qualities = Object.keys(chamberData).map(parseFloat).sort((a, b) => a - b);
        if (quality < qualities[0] || quality > qualities[qualities.length - 1]) return null;
        if (chamberData[quality]) return chamberData[quality];

        for (let i = 0; i < qualities.length - 1; i++) {
            const x0 = qualities[i];
            const x1 = qualities[i + 1];
            if (quality >= x0 && quality <= x1) {
                const y0 = chamberData[x0];
                const y1 = chamberData[x1];
                return interpolate(quality, x0, y0, x1, y1);
            }
        }
        return null;
    }

    function getKsCoefficients(vRatio) {
        const ratios = Object.keys(ksCoefficients).map(parseFloat).sort((a, b) => a - b);
        if (vRatio < ratios[0] || vRatio > ratios[ratios.length - 1]) return null;
        if (ksCoefficients[vRatio]) return ksCoefficients[vRatio];

        for (let i = 0; i < ratios.length - 1; i++) {
            const r0 = ratios[i];
            const r1 = ratios[i + 1];
            if (vRatio >= r0 && vRatio <= r1) {
                const c0 = ksCoefficients[r0];
                const c1 = ksCoefficients[r1];
                const a0 = interpolate(vRatio, r0, c0.a0, r1, c1.a0);
                const a1 = interpolate(vRatio, r0, c0.a1, r1, c1.a1);
                const a2 = interpolate(vRatio, r0, c0.a2, r1, c1.a2);
                return { a0: a0, a1: a1, a2: a2 };
            }
        }
        return null;
    }
    
    function autoFillKq(prefix, quality, chamberModel, dataTable) {
         if (chamberModel === 'Custom') return; // Don't auto-fill for custom
         const kq = lookupKq(quality, chamberModel, dataTable);
         if (kq !== null) {
             setInputValue(`${prefix}-kq`, kq.toFixed(4));
         } else {
             setInputValue(`${prefix}-kq`, '');
         }
    }

    // --- MAIN CALCULATION FUNCTIONS ---
    function calculateDose(prefix) {
        // Auto-fill kQ
         if (prefix === 'p') {
            autoFillKq('p', getNumericValue('p-tpr2010'), getSelectedValue('p-chamber-model'), k_Q_photon_data);
        } else {
            autoFillKq('e', getNumericValue('e-r50'), getSelectedValue('e-chamber-model'), k_Q_electron_data);
        }

        // Electron-specific calculation for z_ref
        if (prefix === 'e') {
            const R50 = getNumericValue('e-r50');
            const z_ref = 0.6 * R50 - 0.1;
            setInputValue('e-depth', z_ref > 0 ? z_ref.toFixed(3) : 'Invalid R₅₀');
        }

        // kTP calculation
        const T = getNumericValue(`${prefix}-temp`);
        const T0 = getNumericValue(`${prefix}-cal-temp`);
        const P = getNumericValue(`${prefix}-pressure`);
        const P0 = getNumericValue(`${prefix}-cal-pressure`);
        const k_TP = P > 0 && T0 > -273.2 ? ((273.2 + T) / (273.2 + T0)) * (P0 / P) : 0;
        setInputValue(`${prefix}-ktp-result`, k_TP.toFixed(5));

        // k_pol calculation
        const M_pos = getNumericValue(`${prefix}-m-pos`);
        const M_neg = getNumericValue(`${prefix}-m-neg`);
        const M1 = getNumericValue(`${prefix}-m1`);
        const k_pol = (M1 > 0) ? (Math.abs(M_pos) + Math.abs(M_neg)) / (2 * M1) : 1.0;
        setInputValue(`${prefix}-kpol-result`, k_pol.toFixed(5));
        
        // k_s calculation
        const V1 = getNumericValue(`${prefix}-v1`);
        const V2 = getNumericValue(`${prefix}-v2`);
        const M2 = getNumericValue(`${prefix}-m2`);
        const coeffsTextElement = document.getElementById(`${prefix}-ks-coeffs`);
        let k_s = 1.0;
        
        if (V1 > 0 && V2 > 0) {
            const vRatio = V1 / V2;
            const coeffs = getKsCoefficients(vRatio);
            if (coeffs) {
                const a0 = coeffs.a0;
                const a1 = coeffs.a1;
                const a2 = coeffs.a2;
                const mRatio = (M1 > 0 && M2 > 0) ? M1 / M2 : 1;
                k_s = a0 + a1 * mRatio + a2 * (mRatio ** 2);
                coeffsTextElement.innerHTML = `Using V₁=${V1}V, V₂=${V2}V (Ratio=${vRatio.toFixed(2)}).<br>Coefficients (interp.): a₀=${a0.toFixed(3)}, a₁=${a1.toFixed(3)}, a₂=${a2.toFixed(3)}`;
            } else {
                k_s = 1.0; 
                coeffsTextElement.textContent = `Note: V₁/V₂ ratio not in table, kₛ defaults to 1.0.`;
            }
        } else {
            coeffsTextElement.textContent = `Note: a₀, a₁, a₂ are automatically determined from the V₁/V₂ ratio.`;
        }
        setInputValue(`${prefix}-ks-result`, k_s.toFixed(5));

        // Final dose calculation
        const k_elec = getNumericValue(`${prefix}-kelec`);
        const M_Q = M1 * k_TP * k_elec * k_pol * k_s;
        setInputValue(`${prefix}-mq-result`, M_Q.toFixed(5));

        const N_D_w = getNumericValue(`${prefix}-ndw`);
        const k_Q = getNumericValue(`${prefix}-kq`);
        const D_w_Q = M_Q * N_D_w * k_Q;
        
        document.getElementById(`${prefix}-dose-result`).textContent = `${D_w_Q.toFixed(5)} Gy/MU`;

        const doseRateMU = getNumericValue(`${prefix}-dose-rate`);
        const doseRate = D_w_Q * doseRateMU;
        document.getElementById(`${prefix}-dose-rate-result`).textContent = `${doseRate.toFixed(3)} Gy/min`;
    }

    // --- EVENT LISTENERS ---
    const photonInputs = document.querySelectorAll('#photon-worksheet input, #photon-worksheet select');
    const electronInputs = document.querySelectorAll('#electron-worksheet input, #electron-worksheet select');
    
    photonInputs.forEach(input => input.addEventListener('input', () => calculateDose('p')));
    electronInputs.forEach(input => input.addEventListener('input', () => calculateDose('e')));
    
    const photonTabButton = document.getElementById('photon-tab-button');
    const electronTabButton = document.getElementById('electron-tab-button');
    const photonWorksheet = document.getElementById('photon-worksheet');
    const electronWorksheet = document.getElementById('electron-worksheet');

    function switchTabs(activeTab, inactiveTab, activeWorksheet, inactiveWorksheet) {
        activeTab.classList.add('active'); inactiveTab.classList.remove('active');
        activeWorksheet.classList.remove('hidden'); inactiveWorksheet.classList.add('hidden');
    }
    photonTabButton.addEventListener('click', () => switchTabs(photonTabButton, electronTabButton, photonWorksheet, electronWorksheet));
    electronTabButton.addEventListener('click', () => switchTabs(electronTabButton, photonTabButton, electronWorksheet, photonWorksheet));

    // --- RESET and INITIALIZATION ---
    function resetForm(formId) {
        const form = document.getElementById(formId);
        const prefix = formId.startsWith('photon') ? 'p' : 'e';
        
        // Set default values from HTML attributes
         form.querySelectorAll('input, select').forEach(input => {
            const defaultValue = input.getAttribute('value');
            if (input.tagName === 'SELECT') {
                const selectedOption = input.querySelector('option[selected]');
                input.selectedIndex = selectedOption ? selectedOption.index : 0;
            } else if (input.type === 'date') {
                // handled separately
            } else if (input.type !== 'button' && !input.readOnly) {
               input.value = defaultValue || '';
            }
        });
        
        // Restore default dates
        setInputValue(`${prefix}-date`, '2025-10-10');
        setInputValue(`${prefix}-cal-date`, prefix === 'p' ? '2025-04-01' : '2025-05-01');

        // Recalculate everything with default values
        calculateDose(prefix);
    }
    
    document.getElementById('p-reset-button').addEventListener('click', () => resetForm('photon-worksheet'));
    document.getElementById('e-reset-button').addEventListener('click', () => resetForm('electron-worksheet'));

     // --- PRINT FUNCTIONALITY ---
    document.getElementById('print-button').addEventListener('click', () => {
        const printModal = document.getElementById('print-modal');
        let reportHTML = '';

        // --- Function to generate table rows from IDs and labels ---
        const createRow = (label, id) => {
            const element = document.getElementById(id);
            let value = element.value;
             if (element.tagName === 'SELECT') {
                value = element.options[element.selectedIndex].text;
            }
            else if(element.tagName === 'P') { // For result <p> tags
                value = element.textContent;
            }

            return `<tr><th>${label}</th><td>${value || 'N/A'}</td></tr>`;
        };
        
         const createKsRow = (prefix) => {
            const V1 = getNumericValue(`${prefix}-v1`);
            const V2 = getNumericValue(`${prefix}-v2`);
            if (V1 > 0 && V2 > 0) {
                const vRatio = V1 / V2;
                const coeffs = getKsCoefficients(vRatio);
                if (coeffs) {
                    return `
                        <tr><th>Recombination Coeff. a₀ (for V₁/V₂=${vRatio.toFixed(2)})</th><td>${coeffs.a0.toFixed(3)}</td></tr>
                        <tr><th>Recombination Coeff. a₁ (for V₁/V₂=${vRatio.toFixed(2)})</th><td>${coeffs.a1.toFixed(3)}</td></tr>
                        <tr><th>Recombination Coeff. a₂ (for V₁/V₂=${vRatio.toFixed(2)})</th><td>${coeffs.a2.toFixed(3)}</td></tr>`;
                }
            }
            return '';
        };
        
        // --- Generate Photon Report ---
        reportHTML += `
            <div class="print-section">
                <h2 class="print-title">Dosimetry Report: High-Energy Photon Beam</h2>
                <h3 class="print-subtitle">General Information</h3>
                <table class="print-table">
                    ${createRow('User', 'p-user')}
                    ${createRow('Date', 'p-date')}
                </table>
                <h3 class="print-subtitle">1. Radiation Unit & Reference Conditions</h3>
                <table class="print-table">
                    ${createRow('Accelerator', 'p-accelerator')}
                    ${createRow('Nominal Accel. Potential (MV)', 'p-potential')}
                    ${createRow('Nominal Dose Rate (MU/min)', 'p-dose-rate')}
                    ${createRow('Beam Quality, Q (TPR₂₀,₁₀)', 'p-tpr2010')}
                    ${createRow('Setup', 'p-setup')}
                    ${createRow('Reference Field Size (cm)', 'p-field-size')}
                    ${createRow('Reference Distance (cm)', 'p-distance')}
                    ${createRow('Reference Depth, z<sub>ref</sub> (g/cm²)', 'p-depth')}
                </table>
                <h3 class="print-subtitle">2. Ionization Chamber & Electrometer</h3>
                <table class="print-table">
                     ${createRow('Ion Chamber Model', 'p-chamber-model')}
                     ${createRow('Chamber Serial No.', 'p-chamber-sn')}
                     ${createRow('Electrometer Model', 'p-electrometer-model')}
                     ${createRow('Electrometer Serial No.', 'p-electrometer-sn')}
                     ${createRow('Calibration Laboratory', 'p-cal-lab')}
                     ${createRow('Calibration Date', 'p-cal-date')}
                     ${createRow('N<sub>D,w,Qo</sub> (Gy/nC)', 'p-ndw')}
                     ${createRow('Calibration Temp, T₀ (°C)', 'p-cal-temp')}
                     ${createRow('Calibration Pressure, P₀ (kPa)', 'p-cal-pressure')}
                </table>
                 <h3 class="print-subtitle">3. Readings & Correction Factors</h3>
                <table class="print-table">
                    ${createRow('Current Temperature, T (°C)', 'p-temp')}
                    ${createRow('Current Pressure, P (kPa)', 'p-pressure')}
                    ${createRow('Electrometer Factor, k<sub>elec</sub>', 'p-kelec')}
                    ${createRow('Reading at +V₁ (M₊)', 'p-m-pos')}
                    ${createRow('Reading at -V₁ (M₋)', 'p-m-neg')}
                    ${createRow('Polarizing Potential, V₁ (V)', 'p-v1')}
                    ${createRow('Second Potential, V₂ (V)', 'p-v2')}
                    ${createRow('Reading at V₁ (M₁)', 'p-m1')}
                    ${createRow('Reading at V₂ (M₂)', 'p-m2')}
                </table>
                 <h3 class="print-subtitle">4. Calculated Results</h3>
                <table class="print-table">
                    ${createRow('Temp/Pressure Factor, k<sub>TP</sub>', 'p-ktp-result')}
                    ${createRow('Polarity Factor, k<sub>pol</sub>', 'p-kpol-result')}
                    ${createKsRow('p')}
                    ${createRow('Recombination Factor, k<sub>s</sub>', 'p-ks-result')}
                    ${createRow('Corrected Reading, M<sub>Q</sub> (nC)', 'p-mq-result')}
                    ${createRow('Beam Quality Factor, k<sub>Q,Qo</sub>', 'p-kq')}
                    <tr class="final-result-print"><th>Absorbed Dose to Water, D<sub>w,Q</sub> (Gy/MU)</th><td>${document.getElementById('p-dose-result').textContent}</td></tr>
                    <tr class="final-result-print"><th>Absorbed Dose Rate (Gy/min)</th><td>${document.getElementById('p-dose-rate-result').textContent}</td></tr>
                </table>
            </div>
        `;

         // --- Generate Electron Report ---
        reportHTML += `
            <div class="print-section">
                <h2 class="print-title">Dosimetry Report: High-Energy Electron Beam</h2>
                <h3 class="print-subtitle">General Information</h3>
                <table class="print-table">
                    ${createRow('User', 'e-user')}
                    ${createRow('Date', 'e-date')}
                </table>
                <h3 class="print-subtitle">1. Radiation Unit & Reference Conditions</h3>
                <table class="print-table">
                    ${createRow('Accelerator', 'e-accelerator')}
                    ${createRow('Nominal Energy (MeV)', 'e-energy')}
                    ${createRow('Nominal Dose Rate (MU/min)', 'e-dose-rate')}
                    ${createRow('Beam Quality, Q (R₅₀ in g/cm²)', 'e-r50')}
                    ${createRow('Reference Field Size (cm)', 'e-field-size')}
                    ${createRow('Reference SSD (cm)', 'e-ssd')}
                    ${createRow('Calculated Reference Depth, z<sub>ref</sub> (g/cm²)', 'e-depth')}
                </table>
                <h3 class="print-subtitle">2. Ionization Chamber & Electrometer</h3>
                <table class="print-table">
                     ${createRow('Ion Chamber Model', 'e-chamber-model')}
                     ${createRow('Chamber Serial No.', 'e-chamber-sn')}
                     ${createRow('Electrometer Model', 'e-electrometer-model')}
                     ${createRow('Electrometer Serial No.', 'e-electrometer-sn')}
                     ${createRow('Calibration Laboratory', 'e-cal-lab')}
                     ${createRow('Calibration Date', 'e-cal-date')}
                     ${createRow('N<sub>D,w,Qo</sub> (Gy/nC)', 'e-ndw')}
                     ${createRow('Calibration Temp, T₀ (°C)', 'e-cal-temp')}
                     ${createRow('Calibration Pressure, P₀ (kPa)', 'e-cal-pressure')}
                </table>
                 <h3 class="print-subtitle">3. Readings & Correction Factors</h3>
                <table class="print-table">
                    ${createRow('Current Temperature, T (°C)', 'e-temp')}
                    ${createRow('Current Pressure, P (kPa)', 'e-pressure')}
                    ${createRow('Electrometer Factor, k<sub>elec</sub>', 'e-kelec')}
                    ${createRow('Reading at +V₁ (M₊)', 'e-m-pos')}
                    ${createRow('Reading at -V₁ (M₋)', 'e-m-neg')}
                    ${createRow('Polarizing Potential, V₁ (V)', 'e-v1')}
                    ${createRow('Second Potential, V₂ (V)', 'e-v2')}
                    ${createRow('Reading at V₁ (M₁)', 'e-m1')}
                    ${createRow('Reading at V₂ (M₂)', 'e-m2')}
                </table>
                 <h3 class="print-subtitle">4. Calculated Results</h3>
                <table class="print-table">
                    ${createRow('Temp/Pressure Factor, k<sub>TP</sub>', 'e-ktp-result')}
                    ${createRow('Polarity Factor, k<sub>pol</sub>', 'e-kpol-result')}
                    ${createKsRow('e')}
                    ${createRow('Recombination Factor, k<sub>s</sub>', 'e-ks-result')}
                    ${createRow('Corrected Reading, M<sub>Q</sub> (nC)', 'e-mq-result')}
                     ${createRow('Beam Quality Factor, k<sub>Q,Qo</sub>', 'e-kq')}
                    <tr class="final-result-print"><th>Absorbed Dose to Water, D<sub>w,Q</sub> (Gy/MU)</th><td>${document.getElementById('e-dose-result').textContent}</td></tr>
                    <tr class="final-result-print"><th>Absorbed Dose Rate (Gy/min)</th><td>${document.getElementById('e-dose-rate-result').textContent}</td></tr>
                </table>
            </div>
        `;

        printModal.innerHTML = reportHTML;
        window.print();
    });

    // Initial calculation on load to populate all fields
    calculateDose('p');
    calculateDose('e');
});