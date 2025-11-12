const express = require("express");
const cors = require("cors");
const { auth } = require("../util/firebase")

const router = express.Router();
router.use(cors());

// all routes are prefixed with /auth
router.post("/register", async (req, res) => {

    const email = req.body.email;
    const password = req.body.password;

    try{
        await auth.createUser({
            email: email,
            password: password
        })

        res.status(200).send("Success!");
        return;
    }catch(error){
        res.status(400).send("Cobalt Server (Error Message): " + error.message);
        return;
    }
    
})

module.exports = router;