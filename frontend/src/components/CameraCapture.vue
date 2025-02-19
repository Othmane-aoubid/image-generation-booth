<template>
  <div class="relative">
    <div v-if="showPreview" class="relative mb-6">
      <video
        ref="video"
        class="w-full h-[400px] object-cover rounded-lg bg-black"
        autoplay
        muted
        playsinline
      ></video>
      <div class="absolute inset-0 rounded-lg ring-1 ring-white/10"></div>
    </div>
    
    <div class="flex justify-between items-center">
      <button
        @click="captureImage"
        :disabled="!selectedModel"
        class="px-6 py-3 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-all duration-200 flex items-center space-x-2"
      >
        <span class="material-icons">photo_camera</span>
        <span>Take Photo</span>
      </button>
    </div>

    <div v-if="!showPreview" class="mt-4 p-4 bg-gray-700/50 rounded-lg">
      <div class="flex items-center space-x-3 text-yellow-400">
        <span class="material-icons">warning</span>
        <p class="text-sm">
          Camera access is required. Please enable it in your browser settings.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  name: "CameraCapture",
  props: {
    selectedModel: {
      type: String,
      default: ""
    }
  },
  data() {
    return {
      showPreview: false,
      stream: null,
      models: [
        {
          id: "model1",
          name: "Style Transfer",
          prompt: "artistic style transfer, vibrant colors, detailed",
        },
        {
          id: "model2",
          name: "Portrait Effects",
          prompt: "professional portrait photography, perfect lighting",
        },
        {
          id: "model3",
          name: "Artistic Filter",
          prompt: "artistic oil painting, bold brushstrokes, expressive",
        },
      ],
      toast: useToast(),
    };
  },
  methods: {
    async initCamera() {
      try {
        this.showPreview = true; // Show video element first
        await this.$nextTick(); // Wait for DOM update

        const video = this.$refs.video;
        if (!video) {
          throw new Error("Video element not found");
        }

        // First check if camera permissions are granted
        const permissions = await navigator.mediaDevices.getUserMedia({
          video: true,
        });
        permissions.getTracks().forEach((track) => track.stop()); // Stop the test stream

        // Now initialize with desired settings
        this.stream = await navigator.mediaDevices.getUserMedia({
          video: {
            facingMode: "environment",
            width: { ideal: 1920 },
            height: { ideal: 1080 },
          },
        });

        video.srcObject = this.stream;

        // Wait for video to be ready with increased timeout
        await Promise.race([
          new Promise((resolve) => {
            video.onloadedmetadata = () => {
              video.play().then(resolve);
            };
          }),
          new Promise((_, reject) =>
            setTimeout(() => reject(new Error("Video initialization timeout")), 15000)
          ),
        ]);

      } catch (error) {
        console.error("Error accessing camera:", error);
        this.showPreview = false;
        
        if (error.name === "NotAllowedError") {
          this.toast.error(
            "Camera access denied. Please enable camera permissions in your browser."
          );
        } else if (error.name === "NotFoundError") {
          this.toast.error(
            "No camera found. Please ensure your device has a camera and try again."
          );
        } else if (
          error.name === "AbortError" ||
          error.message.includes("timeout")
        ) {
          this.toast.error(
            "Camera initialization timed out. Please try again or check your camera settings."
          );
        } else {
          this.toast.error(
            "Failed to initialize camera. Please refresh the page and try again."
          );
        }
        throw error;
      }
    },
    async captureImage() {
      if (!this.selectedModel) {
        this.toast.warning("Please select a model first");
        return;
      }

      const video = this.$refs.video;
      if (!video || !video.videoWidth || !video.videoHeight) {
        this.toast.error("Camera not ready. Please try again.");
        return;
      }

      try {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        // Convert to base64 and emit
        const dataUrl = canvas.toDataURL("image/jpeg");
        this.$emit("image-captured", { dataUrl });
        
      } catch (error) {
        console.error("Error capturing image:", error);
        this.toast.error("Failed to capture image. Please try again.");
      }
    },
  },
  mounted() {
    this.initCamera();
  },
  beforeUnmount() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>
