<template>
  <div>
    <h2 class="text-2xl font-semibold mb-6">Select Style</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
      <div
        v-for="model in models"
        :key="model.id"
        @click="selectModel(model.id)"
        class="group relative bg-gray-800 rounded-lg overflow-hidden cursor-pointer transition-all duration-300 hover:ring-2 hover:ring-purple-500"
      >
        <div class="aspect-w-16 aspect-h-9">
          <img 
            :src="model.preview" 
            :alt="model.name"
            class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
        </div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent opacity-100">
          <div class="absolute bottom-0 left-0 right-0 p-4">
            <h3 class="text-lg font-semibold text-white mb-1">
              {{ model.name }}
            </h3>
            <p class="text-sm text-gray-300">
              {{ model.description }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import VintageImage from "../assets/beach-banner-after-1200px.webp";
import ArtisticImage from "../assets/1_Y50-Ut4Bry8xIaC5YRlbrA.jpg";
import PortraitImage from "../assets/raison-realiser-portrait-professionnel.jpg";
import ColorPopImage from "../assets/wp-2023-12-10-bwcv2-photo-after-1.avif";

export default {
  name: "ImageGrid",
  props: {
    selectedModel: {
      type: String,
      default: ""
    },
    showCamera: Boolean
  },
  data() {
    return {
      models: [
        {
          id: "vintage",
          name: "Vintage Film",
          description:
            "Classic film photography look with warm tones and grain",
          preview: VintageImage,
          prompt:
            "vintage film photography, kodak portra 400, grainy, warm tones",
        },
        {
          id: "artistic",
          name: "Artistic Paint",
          description: "Artistic painting style with bold brushstrokes",
          preview: ArtisticImage,
          prompt:
            "oil painting, impressionist style, bold brushstrokes, artistic",
        },
        {
          id: "portrait",
          name: "Portrait Pro",
          description: "Professional portrait enhancement",
          preview: PortraitImage,
          prompt:
            "professional portrait photography, studio lighting, sharp details",
        },
        {
          id: "color",
          name: "Color Pop",
          description: "Vibrant color enhancement with modern look",
          preview: ColorPopImage,
          prompt: "vibrant colors, modern photography, high contrast, sharp",
        },
      ],
      showPreview: false,
      stream: null,
      toast: useToast(),
      processedImages: [],
    };
  },
  computed: {
    selectedModelName() {
      const selectedModel = this.models.find((model) => model.id === this.selectedModel);
      return selectedModel ? selectedModel.name : "";
    }
  },
  methods: {
    selectModel(modelId) {
      this.$emit("model-selected", modelId);
    },
    async initCamera() {
      try {
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

        // Add timeout protection
        const videoInitTimeout = new Promise((_, reject) => {
          setTimeout(
            () => reject(new Error("Video initialization timeout")),
            10000
          );
        });

        await this.$nextTick();
        const video = this.$refs.video;
        if (!video) {
          throw new Error("Video element not found");
        }

        video.srcObject = this.stream;

        // Wait for video to be ready with timeout
        await Promise.race([
          new Promise((resolve) => (video.onloadedmetadata = resolve)),
          videoInitTimeout,
        ]);

        this.showPreview = true;
      } catch (error) {
        console.error("Error accessing camera:", error);
        if (error.name === "NotAllowedError") {
          this.toast.error(
            "Camera access denied. Please enable camera permissions in your browser."
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
            "Failed to access camera. Please check your camera connection and permissions."
          );
        }
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

        // Convert canvas to blob
        const blob = await new Promise((resolve) =>
          canvas.toBlob(resolve, "image/jpeg", 0.9)
        );

        // Create FormData
        const formData = new FormData();
        formData.append("image", blob, "image.jpg");
        formData.append("model_id", this.selectedModel);
        const selectedModel = this.models.find((model) => model.id === this.selectedModel);
        formData.append("prompt", selectedModel.prompt);

        // Send to backend
        const response = await fetch("http://localhost:5000/generate", {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          throw new Error("Failed to process image");
        }

        const result = await response.json();
        this.processedImages.unshift({
          id: Date.now(),
          original: URL.createObjectURL(blob),
          processed: result.image_url,
          model: selectedModel.name,
        });

        this.toast.success("Image processed successfully!");
      } catch (error) {
        console.error("Error processing image:", error);
        this.toast.error("Failed to process image. Please try again.");
      }
    },
  },
  beforeMount() {
    if (this.selectedModel) {
      this.initCamera();
    }
  },
  beforeUnmount() {
    if (this.stream) {
      this.stream.getTracks().forEach((track) => track.stop());
    }
  },
};
</script>

<style scoped>
.aspect-w-16 {
  position: relative;
  padding-bottom: 56.25%;
}

.aspect-w-16 > * {
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
}
</style>