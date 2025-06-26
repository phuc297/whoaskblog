
btnSave = document.querySelector('#btn-save')
btnNext = document.querySelector('#btn-next')
btnBack = document.querySelector('#btn-back')
btnPublish = document.querySelector('#btn-publish')

postTitleElement = document.querySelector('#id_title')
postMainContentElement = document.querySelector('#post-main-content')
postInfoElement = document.querySelector('#post-info')

btnNext.addEventListener('click', () => {

    if (postTitleElement.value.trim() == '') {
        alert("Please complete all required fields.")
        return
    }

    const content_ql_editor = postMainContentElement.querySelector('.ql-editor');
    const isEmpty = content_ql_editor.innerHTML.trim() === '<p><br></p>';
    if (isEmpty) {
        alert("Content is empty!")
        return
    }

    btnNext.classList.toggle('hidden')
    btnSave.classList.toggle('hidden')
    postMainContentElement.classList.toggle('hidden')


    btnBack.classList.toggle('hidden')
    btnPublish.classList.toggle('hidden')
    postInfoElement.classList.toggle('hidden');


})

btnBack.addEventListener('click', () => {

    btnNext.classList.toggle('hidden')
    btnSave.classList.toggle('hidden')
    postMainContentElement.classList.toggle('hidden')

    btnBack.classList.toggle('hidden')
    btnPublish.classList.toggle('hidden')
    postInfoElement.classList.toggle('hidden');

})

editorForm = document.getElementById('ql-editor-form')
editorForm.addEventListener('submit', () => {

    editorForm.preventDefault();

    let actionInput = document.createElement("input");
    actionInput.type = "hidden";
    actionInput.name = "action";
    actionInput.value = editorForm.submitter.value;
    editorForm.appendChild(actionInput);
    // editorForm.submit()
    console.log(editorForm.action)
    const formData = new FormData(editorForm);
    fetch(editorForm.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': editorForm.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: formData,
    })
        .then(response => {
            if (!response.ok) throw new Error('Lỗi mạng hoặc máy chủ');
            return response.text(); 
        })
        .then(data => {
            if (data.success) {
                
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

})

document.addEventListener('DOMContentLoaded', function () {
    const ql_editors = document.querySelectorAll('.ql-editor')
    ql_editors.forEach((editor) => {
        editor.setAttribute('spellcheck', 'false')
    })
})