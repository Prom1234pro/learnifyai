const scrollers = document.querySelectorAll(".scroller");
if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches){
  addAnimation();
}

function addAnimation() {
  scrollers.forEach((scroller) => {
    scroller.setAttribute("data-animated", true);

    const scrollerInner = scroller.querySelector('.scroller__inner');
    const scrollerContent = Array.from(scrollerInner.children);


    scrollerContent.forEach(item => {
      const duplicatedItem = item.cloneNode(true);
      duplicatedItem.setAttribute("aria-hidden", true);
      scrollerInner.appendChild(duplicatedItem);
    });
  });
};



const searchInput = document.getElementById('search-input');
const searchResults = document.getElementById('search-results');
const startButton = document.getElementById('start-button');

searchInput.addEventListener('click', function() {
  const searchTerm = this.value.trim();
  const matchedSchools = filterSchools(searchTerm);
  displayResults(matchedSchools);
});


let selectedSchool = null;
const schools = [
  { name: 'University of Benin', shortcode: 'UNIBEN' },
  { name: 'Benson Idahosa University', shortcode: 'BIU' },
  { name: 'Igbinedion University Okada', shortcode: 'IUO' },
  { name: 'Ambrose Ali University', shortcode: 'AAU' },

];

function filterSchools(searchTerm) {
  return schools.filter(school => {
    return school.name.toLowerCase().includes(searchTerm.toLowerCase()) || school.shortcode.toLowerCase().includes(searchTerm.toLowerCase());
  });
}

function addUniversity() {
  const newSchoolName = searchInput.value.trim();
  if (newSchoolName === '') return;

  const existingSchool = schools.find(school => school.name.toLowerCase() === newSchoolName.toLowerCase());
  if (!existingSchool) {
    schools.push({ name: newSchoolName, shortcode: '' });
  }

  selectedSchool = schools.find(school => school.name.toLowerCase() === newSchoolName.toLowerCase());
  searchInput.value = selectedSchool.name;
  startButton.disabled = false;
  searchResults.style.display = 'none';
}

function displayResults(matchedSchools) {
  searchResults.innerHTML = '';
  matchedSchools.forEach(school => {
    const button = document.createElement('button');
    button.textContent = school.name;
    button.onclick = function() {
      selectedSchool = school;
      searchInput.value = school.name;
      startButton.disabled = false;
      searchResults.style.display = 'none';
    };
    searchResults.appendChild(button);
  });

  const addUniversityButton = document.createElement('button');
  addUniversityButton.textContent = 'Add University';
  addUniversityButton.onclick = addUniversity;
  searchResults.appendChild(addUniversityButton);

  searchResults.style.display = 'block';
}



searchInput.addEventListener('input', function() {
  const searchTerm = this.value.trim();
  const matchedSchools = filterSchools(searchTerm);
  displayResults(matchedSchools);
});

document.addEventListener('click', function(event) {
  if (!searchResults.contains(event.target) && event.target !== searchInput) {
    searchResults.style.display = 'none';
  }
});

startButton.addEventListener('click', function() {
  window.location.href = 'index.html'; // Redirect to index.html
});


searchInput.addEventListener('input', function() {
    if (this.value.trim() === '') {
      startButton.disabled = true;
    }
  });
  
  function displayResults(matchedSchools) {
    searchResults.innerHTML = '';
    matchedSchools.forEach(school => {
      const button = document.createElement('button');
      button.textContent = school.name;
      button.onclick = function() {
        selectedSchool = school;
        searchInput.value = school.name;
        startButton.disabled = false;
        searchResults.style.display = 'none';
      };
      searchResults.appendChild(button);
    });
  
    const addUniversityButton = document.createElement('button');
    addUniversityButton.textContent = 'Add University';
    addUniversityButton.onclick = addUniversity;
    searchResults.appendChild(addUniversityButton);
  
    searchResults.style.display = 'block';
  }

  function filterSchools(searchTerm) {
    return schools.filter(school => {
      return (school.name.toLowerCase().includes(searchTerm.toLowerCase()) || school.shortcode.toLowerCase().includes(searchTerm.toLowerCase())) && !school.isNew;
    });
  }
  
  function addUniversity() {
    const newSchoolName = searchInput.value.trim();
    if (newSchoolName === '') return;
  
    const existingSchool = schools.find(school => school.name.toLowerCase() === newSchoolName.toLowerCase());
    if (!existingSchool) {
      schools.push({ name: newSchoolName, shortcode: '', isNew: true }); // Mark the new school as isNew
    }
  
    selectedSchool = schools.find(school => school.name.toLowerCase() === newSchoolName.toLowerCase());
    searchInput.value = selectedSchool.name;
    startButton.disabled = false;
    searchResults.style.display = 'none';
  }


  function addUniversity() {
    const newSchoolName = searchInput.value.trim();
    if (newSchoolName === '') return;
  
    const existingSchool = schools.find(school => school.name.toLowerCase() === newSchoolName.toLowerCase());
    if (!existingSchool) {
      schools.push({ name: newSchoolName, shortcode: '', isNew: true }); // Mark the new school as isNew
      selectedSchool = schools[schools.length - 1]; // Set the selected school to the newly added school
    } else {
      selectedSchool = existingSchool;
    }
  
    searchInput.value = selectedSchool.name;
    startButton.disabled = false;
    searchResults.style.display = 'none';
  }
  
  searchInput.addEventListener('input', function() {
    const searchTerm = this.value.trim();
    const matchedSchool = schools.find(school => school.name.toLowerCase() === searchTerm.toLowerCase() && !school.isNew);
  
    if (matchedSchool) {
      selectedSchool = matchedSchool;
      startButton.disabled = false;
    } else {
      startButton.disabled = true;
    }
  });
  
  