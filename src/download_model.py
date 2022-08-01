from transformers import AutoProcessor, AutoModelForPreTraining
processor = AutoProcessor.from_pretrained("facebook/wav2vec2-base")
model = AutoModelForPreTraining.from_pretrained("facebook/wav2vec2-base")
model.save_pretrained("./results/save/wav2vec2_checkpoint")
processor.save_pretrained("./results/save/wav2vec2_checkpoint")