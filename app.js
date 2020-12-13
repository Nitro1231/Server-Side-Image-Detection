const express = require('express');
const cors = require('cors')
const multer = require('multer');

const debug = true;
const port = 5001;

// Initializing App
const app = express();
app.use(cors())

const upload = multer({ dest: 'uploads/', limits: { fileSize: 5 * 1024 * 1024 } });

app.get('/', upload.array('img', 15), (req, res) => {
    res.send('Hello World!');
});

app.post('/items', upload.array('img', 15), (req, res) => {
    console.log(req.files);
});

app.listen(port, () => {
    console.log(`Listening to port http://localhost:${port}/`)
})
