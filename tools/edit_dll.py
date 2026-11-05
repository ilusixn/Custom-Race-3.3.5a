import re
def edit(path, pairs):
    s = open(path, encoding='utf8', newline='').read()
    crlf = '\r\n' in s
    s = s.replace('\r\n', '\n')
    for old, new in pairs:
        assert s.count(old) == 1, (path, old[:60], s.count(old))
        s = s.replace(old, new)
    if crlf: s = s.replace('\n', '\r\n')
    open(path, 'w', encoding='utf8', newline='').write(s)
NAMES = ['Sureki', 'Dreadlord', 'Titan', 'Wretched', 'Fungarian', 'Sporeling', 'Stormforged', 'Moarg', 'Nerubian', 'Lich', 'Mogu', 'LostOne']
DBC = [86, 89, 91, 92, 93, 111, 114, 119, 120, 122, 123, 125]
SK = [18, 10, 9, 64, 11, 11, 13, 8, 8, 7, 12, 9]
edit('CreatureAppearance.h', [
 ("    constexpr bool Uses(unsigned race)\n    {\n        return ", """    // AllRaces v12 pack races (ids 80-91): plain CharSections colour skins bound from EsteriaXxx.bin, skin colour only
    constexpr bool IsPack(unsigned race) { return race >= 80 && race <= 91; }
    inline constexpr unsigned PackSkins[12] = {%s};
    constexpr std::array<Option, 1> PackControl(unsigned race) { return {{ {0, PackSkins[race - 80], 1} }}; }
    inline constexpr std::array<char const*, 1> PackLabels = {{"Skin Color"}};
    constexpr std::array<std::array<Option, 5>, 12> MakePackOptions()
    {
        std::array<std::array<Option, 5>, 12> a{};
        for (unsigned i = 0; i < 12; ++i)
            for (unsigned k = 0; k < 5; ++k)
                a[i][k] = Option{k, k ? 1u : PackSkins[i], 1};
        return a;
    }
    inline constexpr auto PackOptions = MakePackOptions();

    constexpr bool Uses(unsigned race)
    {
        return IsPack(race) || """ % ', '.join(map(str, SK))),
 ("        return Uses(race) && (gender == 0\n", "        return Uses(race) && (IsPack(race) || gender == 0\n"),
 ("            case 78:\n                return FacelessMale;", "            case 78:\n                return FacelessMale;"),
 ("            default:\n                return NagaMale;", "            default:\n                return IsPack(race) ? PackOptions[race - 80] : NagaMale;"),
 ("        if (race >= 77 && race <= 79)\n", "        if (IsPack(race))\n            return fields[0] < options[0].count;\n        if (race >= 77 && race <= 79)\n"),
])
cases = ''.join('        case %d: return %d; // %s (AllRaces v12)\n' % (d, 80 + i, NAMES[i]) for i, d in enumerate(DBC))
cb = ''.join('            case %d: return %s;\n' % (80 + i, NAMES[i].lower()) for i in range(12))
ct = ''.join('            case %d: return L"Esteria%sTextures.bin";\n' % (80 + i, NAMES[i]) for i in range(12))
cf = ''.join('            case %d: return "%s";\n' % (80 + i, NAMES[i]) for i in range(12))
rd = ''.join('        static auto const %s = ReadSelections(L"Esteria%s.bin");\n' % (n.lower(), n) for n in NAMES)
edit('EsteriaAppearance.cpp', [
 ("        case 88: return 79;  // Qiraji (Horde)\n", "        case 88: return 79;  // Qiraji (Horde)\n" + cases),
 ("        static auto const qiraji = ReadSelections(L\"EsteriaQiraji.bin\");\n", "        static auto const qiraji = ReadSelections(L\"EsteriaQiraji.bin\");\n" + rd),
 ("            case 79: return qiraji;\n", "            case 79: return qiraji;\n" + cb),
 ("            case 79: return L\"EsteriaQirajiTextures.bin\";\n", "            case 79: return L\"EsteriaQirajiTextures.bin\";\n" + ct),
 ("            case 79: return \"Qiraji\";\n", "            case 79: return \"Qiraji\";\n" + cf),
 ("        if (RaceOf(CC<unsigned>(character, 0x18)) == 79)\n        {\n            constexpr std::array<VulperaAppearance::Requirement, 0> requirements{};\n            return CC<unsigned>(character, 0x1C)\n                ? HighmountainControl(",
  "        if (CreatureAppearance::IsPack(RaceOf(CC<unsigned>(character, 0x18))))\n        {\n            constexpr std::array<VulperaAppearance::Requirement, 0> requirements{};\n            return HighmountainControl(state, command, character, CreatureAppearance::PackControl(RaceOf(CC<unsigned>(character, 0x18))),\n                CreatureAppearance::PackLabels, requirements);\n        }\n        if (RaceOf(CC<unsigned>(character, 0x18)) == 79)\n        {\n            constexpr std::array<VulperaAppearance::Requirement, 0> requirements{};\n            return CC<unsigned>(character, 0x1C)\n                ? HighmountainControl("),
 ("            if (race == 79)\n                return CC<unsigned>(character, 0x1C)\n                    ? ExtendedGeometry(",
  "            if (CreatureAppearance::IsPack(race))\n                return ExtendedGeometry(character, CreatureAppearance::PackControl(race), RetailSelections(race));\n            if (race == 79)\n                return CC<unsigned>(character, 0x1C)\n                    ? ExtendedGeometry("),
])
edit('HaranirMaterials.inl', [
 ("    if (RaceOf(CC<unsigned>(character, 0x18)) == 79)\n        return;", "    if (RaceOf(CC<unsigned>(character, 0x18)) == 79 || CreatureAppearance::IsPack(RaceOf(CC<unsigned>(character, 0x18))))\n        return;"),
])
print('ok')
