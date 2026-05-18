require('dotenv').config();
const axios = require('axios');
const xml2js = require('xml2js');

async function testKci() {
    try {
        const KCI_API_KEY = process.env.KCI_API_KEY;
        const res = await axios.get('https://open.kci.go.kr/po/openapi/openApiSearch.kci', {
            params: {
                apiCode: 'articleSearch',
                key: KCI_API_KEY,
                title: '유학',
                displayCount: 2
            }
        });
        const parser = new xml2js.Parser({ explicitArray: false });
        const result = await parser.parseStringPromise(res.data);
        console.log(JSON.stringify(result.MetaData.outputData.record, null, 2));
    } catch(err) {
        console.error("Error:", err.message);
    }
}
testKci();
