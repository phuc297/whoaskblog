
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
    if (btnSave) {
        btnSave.classList.toggle('hidden')
    }
    postMainContentElement.classList.toggle('hidden')


    btnBack.classList.toggle('hidden')
    btnPublish.classList.toggle('hidden')
    postInfoElement.classList.toggle('hidden');


})

btnBack.addEventListener('click', () => {

    btnNext.classList.toggle('hidden')
    if (btnSave) {
        btnSave.classList.toggle('hidden')
    }
    postMainContentElement.classList.toggle('hidden')

    btnBack.classList.toggle('hidden')
    btnPublish.classList.toggle('hidden')
    postInfoElement.classList.toggle('hidden');

})

editorForm = document.querySelector('#ql-editor-form')
editorForm.addEventListener('submit', (event) => {

    event.preventDefault();

    let actionInput = document.createElement("input");
    actionInput.type = "hidden";
    actionInput.name = "action";
    actionInput.value = event.submitter.value;
    editorForm.appendChild(actionInput);
    editorForm.submit()

})

document.addEventListener('DOMContentLoaded', function () {
    const ql_editors = document.querySelectorAll('.ql-editor')
    ql_editors.forEach((editor) => {
        editor.setAttribute('spellcheck', 'false')
    })
})