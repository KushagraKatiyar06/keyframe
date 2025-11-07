require('dotenv').config();
const redis=require('../redis');

async function test() {
  await redis.pushJob({ id:'444',prompt:'test video', style:'Meme'});
  console.log('Job pushed successfully!');
  process.exit(0);
}
test();