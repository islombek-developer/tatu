
// function getCookie(name) {

//     return document.cookie.split('; ').find(row => row.startsWith(name + '='))
  
//         ?.split('=')[1];
  
//   }
  
//   const csrftoken = getCookie('csrftoken');
  
//   const questionElements = Array.from(document.querySelectorAll('.box.box-default.question'));
  
//   // Sahifadagi savollarni yig‘ish
  
//   const questionsAndAnswers = questionElements.map((questionEl, index) => ({
  
//     title: questionEl.querySelector('h3.box-title').textContent.trim(),
  
//     index: index
  
//   }));
  
//   // Backend-ga so‘rov yuborish
  
//   fetch("https://eea8-213-230-99-218.ngrok-free.app/api/search/", {
  
//     method: "POST",
  
//     body: JSON.stringify(questionsAndAnswers),
  
//     headers: {
  
//         "Content-type": "application/json; charset=UTF-8",
  
//         "X-CSRFToken": csrftoken
  
//     }
//   })
//   .then(response => response.json())
//   .then(data => {
//     questionElements.forEach((questionEl, index) => {
//         const answerObj = data?.[index]; // Agar mavjud bo'lmasa undefined qaytaradi
//         const answerText = answerObj && Array.isArray(answerObj.answer) 
//             ? answerObj.answer.join(", ") 
//             : "-"; 
//         const questionTextElement = questionEl.querySelector('h3.box-title');
//         const questionText = questionTextElement ? questionTextElement.textContent.trim() : "";
//         if (questionTextElement) {
//             // Javobni savol matniga tasodifiy joyda qo‘shish
//             const randomPosition = Math.floor(Math.random() * (questionText.length + 1));
//             questionTextElement.textContent = 
//                 questionText.slice(0, randomPosition) + 
//                 " (" + answerText + ") " + 
//                 questionText.slice(randomPosition);
//             questionEl.setAttribute("title", answerText);
//         }
//     });
//   })
  
function getCookie(name) {
  return document.cookie.split(`; ${name}=`).pop().split(';').shift();
}

const csrftoken = getCookie('csrftoken');
const questionElements = Array.from(document.querySelectorAll('.box.box-default.question'));
const questionsAndAnswers = questionElements.map((questionEl, index) => ({
  question: questionEl.querySelector('h3.box-title').textContent.trim(),
  index: index + 1,
  answers: Array.from(questionEl.querySelectorAll('.box-body p .qv')).map(answerEl => answerEl.textContent.trim())
}));

fetch("https://eea8-213-230-99-218.ngrok-free.app/api/search/", {
  method: "POST",
  body: JSON.stringify(questionsAndAnswers),
  headers: {
    "Content-type": "application/json; charset=UTF-8",
    "X-CSRFToken": csrftoken
  }
})
.then(response => {
  if (!response.ok) throw new Error('Network response was not ok');
  return response.json();
})
.then(data => {
  questionElements.forEach((questionEl, index) => {
    const answer = data[index]?.answer || "Javob topilmadi";
    const questionTextElement = questionEl.querySelector('h3.box-title');
    const questionText = questionTextElement.textContent.trim();
    const randomPosition = Math.floor(Math.random() * (questionText.length + 1));
    questionTextElement.textContent = questionText.slice(0, randomPosition) + answer + questionText.slice(randomPosition);
    questionEl.setAttribute("title", answer);
  });
})
.catch(error => console.error('Error:', error));