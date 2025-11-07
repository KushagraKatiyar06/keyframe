require('dotenv').config();
const db = require('../database'); 

async function test() {
  await db.createVideosTable();
  const jobId = await db.insertJob('A aligator going to school', 'Meme');
  console.log('Job ID:',jobId);
  
  const job = await db.getJobById(jobId);
  console.log('Job:',job);
  
  await db.closePool();
}

test();
