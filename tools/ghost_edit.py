def rw(p,fn):
    s=open(p,encoding='utf8',newline='').read(); crlf='\r\n' in s; t=fn(s.replace('\r\n','\n'))
    open(p,'w',encoding='utf8',newline='').write(t.replace('\n','\r\n') if crlf else t)
def rep(p,old,new):
    def f(t):
        assert t.count(old)==1,(p,old[:50],t.count(old)); return t.replace(old,new)
    rw(p,f)
rep('Engine/Source/Model2/M2Model.h',"    void UnlinkFromCallbackList();\n};","    void UnlinkFromCallbackList();\n\n    bool m_ghostFx = false; // CoA: translucent spectral look (Elune's Chosen)\n};")
rep('Engine/Source/Model2/M2Model.cpp',"static const uint32_t s_ribbonBlendModes[] = { 0, 1, 2, 10, 3, 4, 5 };\n","""static const uint32_t s_ribbonBlendModes[] = { 0, 1, 2, 10, 3, 4, 5 };

// CoA: spirit look for models flagged m_ghostFx (Elune's Chosen): about half transparent, gently breathing, cold blue tint.
static void M2ApplyGhost(CM2Model* model) {
    if (!model->m_ghostFx) {
        return;
    }

    float t = float(model->m_scene->m_time % 100000) * 0.001f;
    float wave = 0.5f + 0.5f * sinf(t * 1.6f);
    float fade = 0.42f + 0.10f * wave;
    model->m_alpha *= fade;
    model->m_effectiveAlpha *= fade;
    model->m_diffuseColor.x *= 0.80f;
    model->m_diffuseColor.y *= 0.92f;
    model->m_diffuseColor.z *= 1.10f;
    model->m_emissiveColor.x += 0.08f;
    model->m_emissiveColor.y += 0.22f;
    model->m_emissiveColor.z += 0.38f;
}
""")
def f(t):
    loop="    for (uint32_t i = 0; i < data->m_loops.m_count; i++) {\n        uint32_t length = data->m_loops[i].m_length;"
    assert t.count(loop)==2
    t=t.replace(loop,"    M2ApplyGhost(this);\n\n"+loop)
    simple="    *this->m_boneMatrices = M2BodyWorld(this) * scene->m_view; // CoA: body sliders\n    this->m_alpha = this->m_baseAlpha * this->m_fadeAlpha;\n"
    assert t.count(simple)==1
    t=t.replace(simple,simple+"    M2ApplyGhost(this);\n")
    a="    this->m_baseAlpha = 1.0f;\n    this->m_diffuseTintR = 1.0f;"
    assert t.count(a)==1
    return t.replace(a,"    this->m_baseAlpha = 1.0f;\n    this->m_ghostFx = false;\n    this->m_diffuseTintR = 1.0f;")
rw('Engine/Source/Model2/M2Model.cpp',f)
rep('WoW/Common/ComponentCore/RetailRace.h',"void RetailRaceBindOwner(CCharacterComponent* character, CGUnit_C* owner);","void RetailRaceBindOwner(CCharacterComponent* character, CGUnit_C* owner);\nvoid RetailRaceApplyGhost(CCharacterComponent* character); // Elune's Chosen: translucent spectral look")
rep('WoW/Common/ComponentCore/RetailRace.cpp',"void RetailRaceBindOwner(CCharacterComponent* character, CGUnit_C* owner) {\n    if (!character) return;","void RetailRaceApplyGhost(CCharacterComponent* character) {\n    if (!character || character->m_data.m_preferences.m_raceID != 118) return;\n    if (CM2Model* model = character->m_data.m_model) model->m_ghostFx = true;\n}\n\nvoid RetailRaceBindOwner(CCharacterComponent* character, CGUnit_C* owner) {\n    if (!character) return;")
rep('WoW/Common/ComponentCore/RetailRace.cpp',"void RetailRaceBindOwner(CCharacterComponent*, CGUnit_C*) {}","void RetailRaceBindOwner(CCharacterComponent*, CGUnit_C*) {}\nvoid RetailRaceApplyGhost(CCharacterComponent*) {}")
rep('WoW/Common/ComponentCore/CharacterComponent.cpp',"bool CCharacterComponent::RenderPrep(int32_t wait) {\n","bool CCharacterComponent::RenderPrep(int32_t wait) {\n    RetailRaceApplyGhost(this);\n")
print('applied')
