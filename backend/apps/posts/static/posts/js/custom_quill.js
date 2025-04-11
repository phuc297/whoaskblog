const toolbarOptions = [
  [{ 'size': ['normal'] }],

];

const quill = new Quill('#editor-title', {
  modules: {
    toolbar: toolbarOptions
  },
  theme: 'bubble'
});