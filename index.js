import express from "express";
import fs from "fs";

const app = express();
const PORT = process.env.PORT || 3000;

app.get("/search/sgk", (req, res) => {
  const { q } = req.query;

  if (!q) {
    return res.status(400).json({ error: "q parametresi gerekli" });
  }

  try {
    const data = fs.readFileSync("veri.txt", "utf8");
    const satirlar = data.split("\n");
    const sonuc = satirlar.find(s => s.includes(q));

    if (!sonuc) {
      return res.status(404).json({ error: "Veri bulunamadı" });
    }

    return res.json({
      sorgu: q,
      sonuc: sonuc.trim()
    });
  } catch (err) {
    return res.status(500).json({ error: "Dosya okunamadı" });
  }
});

app.listen(PORT, () => {
  console.log("Server çalışıyor:", PORT);
});
