
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'baseword baseword_error double_word initial_letter middle1_word middle1_word_error middle2_word middle_error_word no_word normalword paragraph portugueseTranslation portugueseTranslationError prefix_error_word prefix_word suffix_error_word suffix_wordDict : Alphsection DictDict : Alphsection : initial_letter translationstranslations : normalword portugueseTranslation translationstranslations : baseword portugueseTranslation translationstranslations : '
    
_lr_action_items = {'$end':([0,1,2,3,4,5,8,9,10,11,],[-2,0,-2,-6,-1,-3,-6,-6,-4,-5,]),'initial_letter':([0,2,3,5,8,9,10,11,],[3,3,-6,-3,-6,-6,-4,-5,]),'normalword':([3,8,9,],[6,6,6,]),'baseword':([3,8,9,],[7,7,7,]),'portugueseTranslation':([6,7,],[8,9,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'Dict':([0,2,],[1,4,]),'Alphsection':([0,2,],[2,2,]),'translations':([3,8,9,],[5,10,11,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> Dict","S'",1,None,None,None),
  ('Dict -> Alphsection Dict','Dict',2,'p_dict2','analisesintatica.py',41),
  ('Dict -> <empty>','Dict',0,'p_dict1','analisesintatica.py',45),
  ('Alphsection -> initial_letter translations','Alphsection',2,'p_Alphsection1','analisesintatica.py',49),
  ('translations -> normalword portugueseTranslation translations','translations',3,'p_translations1','analisesintatica.py',53),
  ('translations -> baseword portugueseTranslation translations','translations',3,'p_translations2','analisesintatica.py',57),
  ('translations -> <empty>','translations',0,'p_translations3','analisesintatica.py',61),
]