import re

with open('index2.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the new script
new_script = """<script>
        // The original static dashboardData is now removed.
        // We will fetch real data from our local proxy server.
        let dashboardData = {};
        
        // Show loading spinner
        function showLoading() {
            document.getElementById('tableBody').innerHTML = '<tr><td colspan="5" style="text-align:center; padding: 2rem;">데이터를 불러오는 중입니다...<br><small>(KCI 서버에서 실시간 검색 중)</small></td></tr>';
            document.getElementById('totalPaperCount').innerText = '로딩중...';
        }

        async function fetchKciData(query = '수양론') {
            showLoading();
            try {
                // Fetch up to 100 recent papers to build the dashboard
                const response = await fetch(`http://localhost:3000/api/search?query=${encodeURIComponent(query)}&displayCount=100`);
                const json = await response.json();
                
                if (json.success && json.data.MetaData.outputData.record) {
                    const records = json.data.MetaData.outputData.record;
                    processAndRenderData(Array.isArray(records) ? records : [records]);
                } else {
                    document.getElementById('tableBody').innerHTML = '<tr><td colspan="5" style="text-align:center;">검색 결과가 없습니다.</td></tr>';
                }
            } catch (error) {
                console.error("Error fetching KCI data:", error);
                document.getElementById('tableBody').innerHTML = '<tr><td colspan="5" style="text-align:center; color: #f87171;">서버 통신 중 오류가 발생했습니다. 백엔드 서버가 실행 중인지 확인하세요.</td></tr>';
            }
        }

        function processAndRenderData(records) {
            document.getElementById('totalPaperCount').innerText = records.length;
            
            // 1. Process for Table
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';
            
            records.forEach(record => {
                const tr = document.createElement('tr');
                
                let title = "제목 없음";
                if(record.articleInfo['title-group'] && record.articleInfo['title-group']['article-title']) {
                    const titles = record.articleInfo['title-group']['article-title'];
                    title = Array.isArray(titles) ? titles[0]._ : titles._ || titles;
                }
                
                let author = "저자 미상";
                if(record.articleInfo['author-group'] && record.articleInfo['author-group'].author) {
                    const authors = record.articleInfo['author-group'].author;
                    author = Array.isArray(authors) ? authors.join(', ') : authors;
                }
                
                let journal = record.journalInfo['journal-name'] || "학술지명 없음";
                let year = record.journalInfo['pub-year'] || "";
                let citations = 0;
                if(record['citation-count'] && record['citation-count']._) {
                    citations = record['citation-count']._;
                }
                
                // Try to get link
                let url = record.url || "#";

                tr.innerHTML = `
                    <td><span class="badge">${citations}</span></td>
                    <td><a href="${url}" target="_blank" style="color: var(--text-main); text-decoration: none;">${title}</a></td>
                    <td>${author}</td>
                    <td>${journal}</td>
                    <td>${year}</td>
                `;
                tbody.appendChild(tr);
            });
            
            // Note: Since this is dynamic, we can build charts similarly by aggregating `records`.
            // For now, the existing dashboard framework is maintained, but we replaced the table with real KCI data.
            // Future steps: Update ECharts and Chart.js using aggregated `records` data here.
        }

        // Trigger search when user presses Enter
        document.getElementById('searchInput').addEventListener('keyup', function(e) {
            if(e.key === 'Enter') {
                fetchKciData(this.value);
            }
        });

        // Initial fetch
        window.onload = () => {
            fetchKciData('수양론');
        };
    </script>"""

# Replace the script block
# This regex looks for <script> followed by const dashboardData = ... up to </script>
new_content = re.sub(r'<script>\s*const dashboardData = \{.*?</script>', new_script, content, flags=re.DOTALL)

with open('index2.html', 'w', encoding='utf-8') as f:
    f.write(new_content)
