const express = require("express");
const axios = require("axios");
const bodyParser = require("body-parser");
const path = require("path");

const app = express();
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

const FASTAPI_ENDPOINT = "http://localhost:8001/api/laso";

app.get("/", (req, res) => {
  res.render("index");
});

app.post("/submit", async (req, res) => {
  try {
    const response = await axios.post(FASTAPI_ENDPOINT, req.body);
    res.render("result", { result: response.data });
  } catch (error) {
    res.send("Lỗi: " + error.message);
  }
});

app.listen(3000, () => {
  console.log("✅ Giao diện frontend chạy tại http://localhost:3000");
});
