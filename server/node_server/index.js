require('dotenv').config()
const express = require("express");
const cors = require("cors");
const cron = require("node-cron");

const app = express();
const PORT = process.env.PORT || 5000;

const authRoute = require("./routes/auth.js");

//
app.use(express.json());
app.use(cors());

app.use("/auth", authRoute);


// homepage to test if the server is running correctly
app.get("/", async (req, res) => {
    res.send("The node server is running");
})

app.listen(PORT, ()=> {
    console.log(`server is listing on port ${PORT}`);
})


// use node-cron to keep the node server and python server running
cron.schedule("0 */12 * * * *", () => {
    // make a call every 12 minutes
    // run node server
    fetch(process.env.NODE_SERVER_URL)
    .then(res => res.text())
    .then(data => console.log(data))
    .catch(err => console.log(err))

    // run python server
    fetch(process.env.PYTHON_SERVER_URL)
    .then(res => res.text())
    .then(data => console.log(data))
    .catch(err => console.log(err))
})
