cv.onRuntimeInitialized = () => {
    const video = document.getElementById('videoElement');
    const canvas = document.getElementById('canvasElement');
    const ctx = canvas.getContext('2d');
    let yellowObjects = [];

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.play();
            detectYellow();
        })
        .catch(error => console.error('Error accessing camera:', error));

    function detectYellow() {
        const cap = new cv.VideoCapture(video);
        const frame = new cv.Mat(video.height, video.width, cv.CV_8UC4);

        const yellowLower = new cv.Scalar(20, 100, 100);
        const yellowUpper = new cv.Scalar(30, 255, 255);

        const FPS = 30;

        function processVideo() {
            cap.read(frame);
            cv.cvtColor(frame, frame, cv.COLOR_RGBA2RGB);
            const blurred = new cv.Mat();
            cv.medianBlur(frame, blurred, 5);
            const hsv = new cv.Mat();
            cv.cvtColor(blurred, hsv, cv.COLOR_RGB2HSV);
            const mask = new cv.Mat();
            cv.inRange(hsv, yellowLower, yellowUpper, mask);
            const contours = new cv.MatVector();
            const hierarchy = new cv.Mat();
            cv.findContours(mask, contours, hierarchy, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE);

            yellowObjects = [];

            for (let i = 0; i < contours.size(); i++) {
                const cnt = contours.get(i);
                const area = cv.contourArea(cnt);
                if (area > 100) { // Adjust this threshold as needed
                    const rect = cv.boundingRect(cnt);
                    yellowObjects.push(rect);
                    cv.rectangle(frame, rect, [0, 255, 0, 255], 2);
                }
                cnt.delete();
            }

            contours.delete();
            hierarchy.delete();
            mask.delete();
            hsv.delete();
            blurred.delete();

            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
            requestAnimationFrame(processVideo);
        }

        // Start the processing loop
        setTimeout(() => requestAnimationFrame(processVideo), 1000 / FPS);
    }
};
