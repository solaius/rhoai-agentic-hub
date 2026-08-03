var currentRegisterSkill = null;

function openRegisterModal() {
  if (!currentRegisterSkill) return;
  var s = currentRegisterSkill;
  document.getElementById('reg-skill-name').value = s.name;
  document.getElementById('reg-version').value = s.version;
  document.getElementById('reg-pack').value = s.pack;
  document.getElementById('reg-description').value = s.description;
  var tagsDiv = document.getElementById('reg-tags');
  var tags = [s.pack, s.persona, s.category, s.trustTier, s.signing];
  if (s.apis.length) tags.push.apply(tags, s.apis.map(function(a){ return a.replace(/\s+/g, '-').toLowerCase(); }));
  tagsDiv.innerHTML = tags.map(function(t){
    return '<span class="pf-v6-c-label pf-m-outline pf-m-compact"><span class="pf-v6-c-label__content">'+t+'</span></span>';
  }).join('');
  document.getElementById('reg-namespace').value = 'default';
  document.getElementById('register-modal-backdrop').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('register-modal-backdrop').classList.add('hidden');
}

function submitModal() {
  var name = document.getElementById('reg-skill-name').value;
  var ns = document.getElementById('reg-namespace').value;
  alert('Skill "' + name + '" registered to namespace "' + ns + '" successfully.');
  closeModal();
}

function resetModalForm() {
  document.getElementById('reg-namespace').value = 'default';
}