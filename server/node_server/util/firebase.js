const { initializeApp, cert } = require("firebase-admin/app");
const { getAuth } = require("firebase-admin/auth")

firebaseConfig = {
    "type" : process.env.TYPE,
    "project_id" : process.env.PROJECT_ID,
    "private_key_id" : process.env.PRIVATE_KEY_ID,
    "private_key" : process.env.PRIVATE_KEY.replace(/\\n/g, '\n'),
    "client_email" : process.env.CLIENT_EMAIL,
    "client_id" : process.env.CLIENT_ID,
    "auth_uri" : process.env.AUTH_URI,
    "token_uri" : process.env.TOKEN_URI,
    "auth_provider_x509_cert_url" : process.env.AUTH_PROVIDER_X509_CERT_URL,
    "client_x509_cert_url" : process.env.CLIENT_X509_CERT_URL,
    "universe_domain" : process.env.UNIVERSE_DOMAIN
}

const app = initializeApp({
    credential: cert(firebaseConfig),
    databaseURL: process.env.DATABASE_URL
});

auth = getAuth();

module.exports = {auth: auth}