const toolbarOptions = [
  [{ 'size': ['normal'] }],

];

const quill_title = new Quill('#editor-title', {
  modules: {
    toolbar: toolbarOptions
  },
  theme: 'bubble'
});

const quill_description = new Quill('#editor-description', {
  modules: {
    toolbar: toolbarOptions
  },
  theme: 'bubble'
});