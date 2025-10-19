const express = require('express');
const router = express.Router();
const db = require('../database');

router.get('/', async (req,res) =>{
  try {
    //get the last 20 completed videos from postgres
    const videos = await db.getRecentCompletedVideos();

    //return the videos array
    res.status(200).json({
      success: true,
      count: videos.length,
      videos: videos
    });
    
  } catch (error) {
    console.error('Error in feed route:',error);
    res.status(500).json({ 
      error: 'Failed to get video feed' 
    });}
});

module.exports = router;