<template>
  <div class="container mx-auto p-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div 
        v-for="model in models" 
        :key="model.id"
        @click="selectModel(model)"
        class="card"
        :class="{'card-selected': selectedModel?.id === model.id}"
      >
        <img 
          :src="model.preview" 
          :alt="model.name"
          class="card-image"
        />
        <div class="card-content">
          <h3 class="card-title">{{ model.name }}</h3>
          <p class="card-description">{{ model.description }}</p>
        </div>
      </div>
    </div>

    <!-- Camera Section -->
    <div v-if="selectedModel" class="fixed bottom-0 left-0 right-0 p-4 bg-white shadow-lg">
      <div class="max-w-4xl mx-auto">
        <div v-if="showPreview" class="relative mb-4">
          <video 
            ref="video"
            class="w-full h-64 object-cover rounded-lg"
            autoplay
            muted
            playsinline
          ></video>
        </div>
        <div class="flex justify-between items-center">
          <div class="flex items-center">
            <span class="text-lg font-medium">Selected Model: {{ selectedModel.name }}</span>
          </div>
          <button 
            @click="captureImage" 
            class="btn-primary"
          >
            <span class="material-icons mr-2">photo_camera</span>
            Take Photo
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import VintageImage from '../assets/beach-banner-after-1200px.webp';
import ArtisticImage from '../assets/1_Y50-Ut4Bry8xIaC5YRlbrA.jpg';
import PortraitImage from '../assets/raison-realiser-portrait-professionnel.jpg';
import ColorPopImage from '../assets/wp-2023-12-10-bwcv2-photo-after-1.avif';

export default {
  name: 'ImageGrid',
  data() {
    return {
      models: [
        {
          id: 'vintage',
          name: 'Vintage Film',
          description: 'Classic film photography look with warm tones and grain',
          preview: VintageImage,
          prompt: 'vintage film photography, kodak portra 400, grainy, warm tones'
        },
        {
          id: 'artistic',
          name: 'Artistic Paint',
          description: 'Artistic painting style with bold brushstrokes',
          preview: ArtisticImage,
          prompt: 'oil painting, impressionist style, bold brushstrokes, artistic'
        },
        {
          id: 'portrait',
          name: 'Portrait Pro',
          description: 'Professional portrait enhancement',
          preview: PortraitImage,
          prompt: 'professional portrait photography, studio lighting, sharp details'
        },
        {
          id: 'color',
          name: 'Color Pop',
          description: 'Vibrant color enhancement with modern look',
          preview: ColorPopImage,
          prompt: 'vibrant colors, modern photography, high contrast, sharp'
        }
      ],
      selectedModel: null,
      showPreview: false,
      stream: null,
      toast: useToast()
    }
  },
  methods: {
    selectModel(model) {
      this.selectedModel = model;
      if (!this.stream) {
        this.initCamera();
      }
    },
    async initCamera() {
      try {
        this.stream = await navigator.mediaDevices.getUserMedia({ 
          video: { 
            facingMode: 'environment',
            width: { ideal: 1920 },
            height: { ideal: 1080 }
          } 
        });
        const video = this.$refs.video;
        video.srcObject = this.stream;
        await new Promise(resolve => video.onloadedmetadata = resolve);
        this.showPreview = true;
      } catch (error) {
        console.error('Error accessing camera:', error);
        this.toast.error('Camera access is required for this feature. Please enable camera permissions.');
      }
    },
    async captureImage() {
      const video = this.$refs.video;
      if (!video.videoWidth || !video.videoHeight) {
        this.toast.error('Camera not ready. Please try again.');
        return;
      }

      const canvas = document.createElement('canvas');
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      canvas.getContext('2d').drawImage(video, 0, 0);
      
      try {
        const blob = await new Promise(resolve => {
          canvas.toBlob(resolve, 'image/jpeg', 0.9)
        });
        
        const formData = new FormData();
        formData.append('image', blob, 'capture.jpg');
        formData.append('model', this.selectedModel.id);
        formData.append('prompt', this.selectedModel.prompt);
        
        // TODO: Add API call to your Stable Diffusion backend here
        // const response = await fetch('/api/generate', {
        //   method: 'POST',
        //   body: formData
        // });
        
        this.$emit('image-captured', { 
          blob, 
          model: this.selectedModel,
          dataUrl: canvas.toDataURL('image/jpeg', 0.9)
        });
        
        this.toast.success('Image captured successfully!');
      } catch (error) {
        console.error('Error capturing image:', error);
        this.toast.error('Failed to capture image. Please try again.');
      }
    }
  },
  beforeUnmount() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
    }
  }
}
</script>

<style scoped>
.card {
  @apply bg-white rounded-lg overflow-hidden shadow-lg transition-all duration-300 cursor-pointer hover:shadow-xl;
}

.card-selected {
  @apply ring-2 ring-blue-500;
}

.card-image {
  @apply w-full h-48 object-cover;
}

.card-content {
  @apply p-4;
}

.card-title {
  @apply text-xl font-semibold mb-2;
}

.card-description {
  @apply text-gray-600 text-sm;
}

.btn-primary {
  @apply px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 
         focus:outline-none focus:ring-2 focus:ring-blue-500 
         flex items-center;
}
</style>
