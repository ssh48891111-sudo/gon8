require('dotenv').config();
const axios = require('axios');

async function testKci() {
    try {
        const KCI_API_KEY = process.env.KCI_API_KEY;
        const res = await axios.get('https://open.kci.go.kr/po/openapi/openApiSearch.kci', {
            params: {
                apiCode: 'articleSearch',
                key: KCI_API_KEY,
                title: '유학',
                displayCount: 5
            }
        });
        console.log("Success:", res.data.substring(0, 500)); // Only print part
    } catch(err) {
        if(err.response) {
            console.error("Error data:", err.response.data);
        } else {
            console.error("Error:", err.message);
        }
    }
}
testKci();
