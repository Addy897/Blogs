<script>

    
    import { onMount } from 'svelte';
   
    let editor;
    export let changed=false;
    export let toolbarOptions=[
            [{ 'header': [1, 2, false] }],
            ['bold', 'italic', 'underline'],
            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
            ['image','video']
          ]
    export let f=[];
    export let htmlContent;
    export let delta;
    onMount(async () => {
    const {default:Quill} = await import('quill');
      editor = new Quill('#editor', {
        theme: 'snow',
        modules: {
          toolbar: toolbarOptions
        },
      });
      const Delta = Quill.import("delta")
      if(typeof(delta)==="string"){

          delta= JSON.parse(delta.replaceAll("True","true").replaceAll("False","false"))

          if(delta.ops){
            delta=delta.ops
          }
       
      }
      
      editor.setContents(delta);
      htmlContent=editor.getSemanticHTML();
      editor.on('text-change', function(de, oldDelta, source) {
        changed=true
        htmlContent=editor.getSemanticHTML();
        delta= editor.getContents();
      })
      editor.getModule('toolbar').addHandler('image', () => {
        const MAX_IMAGES = 3;
        const MAX_IMAGE_SIZE_MB = 2;
  
        const totalImages = editor.root.querySelectorAll('img').length;
        if (totalImages >= MAX_IMAGES) {
          alert('You can upload a maximum of ' + MAX_IMAGES + ' images.');
          return;
        }
  
        const input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');
        input.click();
  
        input.onchange = async () => {
          const file = input.files[0];
          
          if (!file.type.startsWith('image/')) {
            alert('Please select an image file.');
            return;
          }
  
          if (file.size > MAX_IMAGE_SIZE_MB * 1024 * 1024) {
            alert('The image size exceeds ' + MAX_IMAGE_SIZE_MB + 'MB.');
            return;
          }
          f = [...f, file];
          const formData = new FormData();
          formData.append('image', file);
          
          const reader = new FileReader()
          
          reader.onload = (e) => {
                const imageUrl = e.target.result;
                editor.focus();
                const range = editor.getSelection();
                editor.insertEmbed(range.index, 'image',imageUrl, Quill.sources.USER);
          }
          
          reader.readAsDataURL(file);
          
          
          
        };
      });
    });
  </script>
  <svelte:head>
  <link href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css" rel="stylesheet">
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
  </svelte:head>
  <style>

    #editor {
      min-height: 300px;
      width: 100%;
    }
    
  
   

  </style>
  
  <div id="editor"></div>
  