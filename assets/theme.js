(function(){
  var root = document.documentElement;
  document.querySelectorAll('[data-theme-toggle]').forEach(function(b){
    b.addEventListener('click', function(){
      var next = root.getAttribute('data-theme') === 'light' ? 'dark' : 'light';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('sk-theme', next); } catch (e) {}
    });
  });
})();
