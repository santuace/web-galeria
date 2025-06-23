
require('dotenv').config();
const fs = require('fs');
const path = require('path');
const axios = require('axios');

const apiKey = process.env.OPENAI_API_KEY;
const imageFolder = path.join(__dirname, 'imagenes'); // lee desde tu carpeta
const outputFile = path.join(__dirname, 'output.csv');

async function analyzeImage(imagePath) {
  try {
    const base64Image = fs.readFileSync(imagePath, { encoding: 'base64' });

    const response = await axios.post(
      'https://api.openai.com/v1/chat/completions',
      {
        model: 'gpt-4o',
        messages: [
          {
            role: 'user',
            content: [
              { type: 'text', text: 'Describí esta imagen y generá un prompt para recrearla visualmente.' },
              { type: 'image_url', image_url: { url: `data:image/jpeg;base64,${base64Image}` } },
            ],
          },
        ],
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
        },
      }
    );

    const output = response.data.choices[0].message.content.trim();
    return output;
  } catch (error) {
    console.error(`Error con ${path.basename(imagePath)}:`, error.response?.data || error.message);
    return null;
  }
}

async function main() {
  const images = fs.readdirSync(imageFolder).filter(file =>
    ['.jpg', '.jpeg', '.png'].includes(path.extname(file).toLowerCase())
  );

  const results = [];

  for (const image of images) {
    console.log(`🧠 Procesando ${image}...`);
    const result = await analyzeImage(path.join(imageFolder, image));
    if (result) {
      results.push([image, result]);
    }
  }

  const csv = 'Imagen,Descripción + Prompt\n' + results.map(r => `"\${r[0]}","\${r[1].replace(/"/g, '""')}"`).join('\n');
  fs.writeFileSync(outputFile, csv);
  console.log(`✅ Archivo generado: \${outputFile}`);
}

main();
