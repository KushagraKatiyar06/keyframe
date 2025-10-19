// src/app/api/v1/status/[JobId]/route.js


"use client";

import { useEffect, useState, useCallback } from 'react';


interface JobStatus {
    jobId: string;
    status: 'QUEUED' | 'PROCESSING' | 'COMPLETE' | 'ERROR';
    progress: number;
    videoUrl: string | null;
    thumbnailUrl: string | null;
}

interface FeedVideo {
    id: string;
    title: string;
    style: string;
    thumbnailUrl: string;
    videoUrl: string;
}


export default function StatusPage({ params }: { params: { jobId: string } }) {

    const [jobStatus, setJobStatus] = useState<JobStatus | null>(null);
    const [feed, setFeed] = useState<FeedVideo[]>([]);
    const [error, setError] = useState<string | null>(null);

    const jobId = params.jobId;


    const fetchStatus = useCallback(async () => {
        if (!jobId) {
            setError("Job ID is missing.");
            return;
        }
        try {
            const res = await fetch(`/api/v1/status/${jobId}`);
            if (!res.ok) {

                throw new Error(`Status check failed: ${res.status}`);
            }
            const data: JobStatus = await res.json();
            setJobStatus(data);
        } catch (err) {
            console.error("Polling error:", err);
            setError("Could not retrieve job status.");
        }
    }, [jobId]);

    const fetchFeed = useCallback(async () => {
        try {
            const res = await fetch('/api/v1/feed');
            if (!res.ok) {
                throw new Error(`Feed fetch failed: ${res.status}`);
            }
            const data: FeedVideo[] = await res.json();
            setFeed(data);
        } catch (err) {
            console.error("Feed error:", err);
        }
    }, []);

    useEffect(() => {
        fetchStatus();
        fetchFeed();

        const intervalId = setInterval(() => {
            if (jobStatus?.status === 'COMPLETE' || jobStatus?.status === 'ERROR') {
                clearInterval(intervalId);
                return;
            }
            fetchStatus();
        }, 5000);

        return () => clearInterval(intervalId);
    }, [fetchStatus, fetchFeed, jobStatus?.status]);

    const CommunityFeed = () => (

        <div className="bg-gray-100 p-4 rounded-lg shadow-inner mt-6" style={{ background: '#333', color: 'white' }}>
            <h2 className="text-xl font-semibold mb-3" style={{ color: '#FFC8D2' }}>
                While You Wait: Community Feed
            </h2>
            <div className="space-y-4 max-h-96 overflow-y-auto">
                {feed.map((video) => (
                    <div key={video.id} className="p-3 bg-white rounded-lg shadow flex items-center" style={{ background: '#444', color: 'white', border: '1px solid #555' }}>
                        <div className="flex-shrink-0 w-16 h-10 bg-gray-300 rounded overflow-hidden mr-3" style={{ background: '#222' }}>
                            <p className="text-xs text-center pt-2" style={{ color: '#E00055' }}>🖼️</p>
                        </div>
                        <div>
                            <p className="font-medium">{video.title}</p>
                            <span className="text-sm italic" style={{ color: '#aaa' }}>Style: {video.style}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );

    if (jobStatus?.status === 'COMPLETE' && jobStatus.videoUrl) {
        return (
            <main className="flex min-h-screen flex-col items-center p-12" style={{ paddingTop: '6rem' }}>
                <h1 className="text-4xl font-bold mb-4" style={{ color: '#00cc00' }}>
                    Video Generation COMPLETE! 🎉
                </h1>
                <div className="w-full max-w-4xl p-6 rounded-xl shadow-lg" style={{ background: '#222' }}>
                    <h2 className="text-2xl font-semibold mb-4" style={{ color: 'white' }}>Video Preview</h2>
                    <div className="aspect-video bg-black rounded-lg overflow-hidden mb-6">
                        <video
                            controls
                            src={jobStatus.videoUrl}
                            poster={jobStatus.thumbnailUrl || undefined}
                            className="w-full h-full object-contain"
                        >
                            Your browser does not support the video tag.
                        </video>
                    </div>
                    <div className="text-center">
                        <a
                            href={jobStatus.videoUrl}
                            download={`keyframe-video-${jobId}.mp4`}
                            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white"
                            style={{ background: '#E00055' }}
                        >
                            Download Final Video
                        </a>
                    </div>
                </div>
            </main>
        );
    }


    return (
        <main className="flex min-h-screen flex-col items-center p-12" style={{ paddingTop: '6rem' }}>
            <h1 className="text-4xl font-bold mb-8" style={{ color: 'white' }}>
                Processing Your Video...
            </h1>

            <div className="w-full max-w-2xl p-8 rounded-xl shadow-lg" style={{ background: '#222' }}>
                <p className="text-lg font-medium mb-2" style={{ color: 'white' }}>
                    Job ID: <span className="font-mono p-1 rounded text-sm" style={{ background: '#111' }}>{jobId}</span>
                </p>

                {error && <p className="font-medium text-center mb-4" style={{ color: '#F87171' }}>{error}</p>}

                {/* Status Display */}
                <div className="mb-4">
                    <p className="text-xl font-semibold mb-1" style={{ color: 'white' }}>
                        Status: {jobStatus ? jobStatus.status : 'Loading...'}
                    </p>
                    <div className="w-full rounded-full h-2.5" style={{ background: '#444' }}>
                        <div
                            className="h-2.5 rounded-full transition-all duration-500"
                            style={{ width: `${jobStatus ? jobStatus.progress : 0}%`, background: '#FF5757' }}
                        ></div>
                    </div>
                    <p className="text-sm mt-1 text-right" style={{ color: '#aaa' }}>
                        {jobStatus?.progress}% Complete
                    </p>
                </div>

                <p className="text-center italic" style={{ color: '#aaa' }}>
                    The AI Worker is currently generating the script, images, and audio. This can take 1-5 minutes.
                </p>

                {/* The "While You Wait" Community Feed */}
                <CommunityFeed />
            </div>
        </main>
    );
}