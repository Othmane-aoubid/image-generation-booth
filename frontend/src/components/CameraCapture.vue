<template>
  <div class="fixed bottom-0 left-0 right-0 p-4 bg-white shadow-lg">
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
        <select 
          v-model="selectedModel" 
          class="p-2 border rounded-lg bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        >
          <option value="" disabled>Select Model</option>
          <option v-for="model in models" :key="model.id" :value="model.id">
            {{ model.name }}
          </option>
        </select>
        <button 
          @click="captureImage" 
          class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 flex items-center"
          :disabled="!selectedModel"
        >
          <span class="material-icons mr-2">photo_camera</span>
          Take Photo
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";

export default {
  name: 'CameraCapture',
  data() {
    return {
      showPreview: false,
      selectedModel: '',
      stream: null,
      models: [
        { 
          id: 'model1', 
          name: 'Style Transfer',
          prompt: 'artistic style transfer, vibrant colors, detailed'
        },
        { 
          id: 'model2', 
          name: 'Portrait Effects',
          prompt: 'professional portrait photography, perfect lighting'
        },
        { 
          id: 'model3', 
          name: 'Artistic Filter',
          prompt: 'artistic oil painting, bold brushstrokes, expressive'
        }
      ],
      toast: useToast()
    }
  },
  methods: {
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
      if (!this.selectedModel) {
        this.toast.warning('Please select a model first');
        return;
      }

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
        formData.append('model', this.selectedModel);
        
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
        this.$emit('capture-error', error);
        this.toast.error('Failed to capture image. Please try again.');
      }
    }
  },
  mounted() {
    this.initCamera();
  },
  beforeUnmount() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
    }
  }
}
</script>
