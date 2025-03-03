// HTML Templates
const converterTemplate = `
    <div id="converterApp" class="hidden">
        <h1>Document Converter</h1>
        
        <div class="converter-tabs">
            <button class="tab-btn active" onclick="converter.showTab('pdfToDocx')">PDF to DOCX</button>
            <button class="tab-btn" onclick="converter.showTab('docxToPdf')">DOCX to PDF</button>
        </div>
        
        <div id="pdfToDocxTab" class="converter-tab">
            <h2>Convert PDF to DOCX</h2>
            <form id="pdfToDocxForm" class="converter-form">
                <div class="file-upload">
                    <label for="pdfFile">Select PDF File</label>
                    <input type="file" id="pdfFile" accept=".pdf" required>
                    <span class="file-name" id="pdfFileName">No file selected</span>
                </div>
                <button type="submit" class="convert-btn">Convert to DOCX</button>
            </form>
        </div>
        
        <div id="docxToPdfTab" class="converter-tab hidden">
            <h2>Convert DOCX to PDF</h2>
            <form id="docxToPdfForm" class="converter-form">
                <div class="file-upload">
                    <label for="docxFile">Select DOCX File</label>
                    <input type="file" id="docxFile" accept=".docx,.doc" required>
                    <span class="file-name" id="docxFileName">No file selected</span>
                </div>
                <button type="submit" class="convert-btn">Convert to PDF</button>
            </form>
        </div>
        
        <div id="conversionResults" class="hidden">
            <h3>Conversion Complete</h3>
            <div class="result-info">
                <p>Your file has been successfully converted!</p>
                <button id="downloadBtn" class="download-btn">Download Converted File</button>
            </div>
        </div>
        
        <button onclick="auth.logout()" class="logout-btn">Logout</button>
    </div>
`;

const converter = {
    currentFileId: null,
    currentFileName: null,
    downloadInProgress: false,

    init() {
        if (!$('#converterApp').length) {
            $('#app').append(converterTemplate);
        }

        // ✅ Remove old event listeners before adding new ones
        $('#pdfToDocxForm').off().on('submit', (e) => {
            e.preventDefault();
            this.convertPdfToDocx();
        });

        $('#docxToPdfForm').off().on('submit', (e) => {
            e.preventDefault();
            this.convertDocxToPdf();
        });

        $('#downloadBtn').off().on('click', (e) => {
            e.preventDefault();
            if (!this.downloadInProgress) {
                this.downloadConvertedFile();
            }
        });

        $('#pdfFile').off().on('change', function() {
            const fileName = $(this).val().split('\\').pop();
            $('#pdfFileName').text(fileName || 'No file selected');
        });

        $('#docxFile').off().on('change', function() {
            const fileName = $(this).val().split('\\').pop();
            $('#docxFileName').text(fileName || 'No file selected');
        });
    },

    showTab(tabName) {
        $('.converter-tab').addClass('hidden');
        $('.tab-btn').removeClass('active');

        if (tabName === 'pdfToDocx') {
            $('#pdfToDocxTab').removeClass('hidden');
            $('.tab-btn:first-child').addClass('active');
        } else {
            $('#docxToPdfTab').removeClass('hidden');
            $('.tab-btn:last-child').addClass('active');
        }

        $('#conversionResults').addClass('hidden');
    },

    convertPdfToDocx() {
        const fileInput = $('#pdfFile')[0];
        if (!fileInput.files.length) {
            alert('Please select a PDF file');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // ✅ Prevent multiple clicks
        const submitBtn = $('#pdfToDocxForm button[type="submit"]');
        if (submitBtn.hasClass('loading')) return;

        const originalText = submitBtn.text();
        submitBtn.text('Converting...').addClass('loading').prop('disabled', true);

        $.ajax({
            url: `${API_BASE_URL}/pdf-to-docx`,
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` },
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                submitBtn.text(originalText).removeClass('loading').prop('disabled', false);
                this.currentFileId = response.file_id;
                this.currentFileName = file.name.replace('.pdf', '.docx');
                $('#conversionResults').removeClass('hidden');
            },
            error: (xhr) => {
                submitBtn.text(originalText).removeClass('loading').prop('disabled', false);
                alert('Conversion failed: ' + (xhr.responseText || 'Unknown error'));
            }
        });
    },

    convertDocxToPdf() {
        const fileInput = $('#docxFile')[0];
        if (!fileInput.files.length) {
            alert('Please select a DOCX file');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // ✅ Prevent multiple clicks
        const submitBtn = $('#docxToPdfForm button[type="submit"]');
        if (submitBtn.hasClass('loading')) return;

        const originalText = submitBtn.text();
        submitBtn.text('Converting...').addClass('loading').prop('disabled', true);

        $.ajax({
            url: `${API_BASE_URL}/docx-to-pdf`,
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken}` },
            data: formData,
            processData: false,
            contentType: false,
            success: (response) => {
                submitBtn.text(originalText).removeClass('loading').prop('disabled', false);
                this.currentFileId = response.file_id;
                this.currentFileName = file.name.replace(/\.docx?$/, '.pdf');
                $('#conversionResults').removeClass('hidden');
            },
            error: (xhr) => {
                submitBtn.text(originalText).removeClass('loading').prop('disabled', false);
                alert('Conversion failed: ' + (xhr.responseText || 'Unknown error'));
            }
        });
    },

    downloadConvertedFile() {
        if (!this.currentFileId) {
            alert('No file available for download');
            return;
        }

        if (this.downloadInProgress) return;

        this.downloadInProgress = true;

        const downloadBtn = $('#downloadBtn');
        const originalText = downloadBtn.text();
        downloadBtn.text('Downloading...').addClass('loading').prop('disabled', true);

        const downloadUrl = `${API_BASE_URL}/download/${this.currentFileId}`;

        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        document.body.appendChild(iframe);

        const form = document.createElement('form');
        form.method = 'GET';
        form.action = downloadUrl;
        form.target = 'download_iframe';

        document.body.appendChild(form);

        setTimeout(() => {
            downloadBtn.text(originalText).removeClass('loading').prop('disabled', false);
            this.downloadInProgress = false;

            setTimeout(() => {
                document.body.removeChild(form);
                document.body.removeChild(iframe);
            }, 5000);
        }, 3000);

        form.submit();
    }
};
