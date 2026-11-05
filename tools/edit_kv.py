import re
p='KvOutfits.inl'; s=open(p,encoding='utf-8',newline='').read()
nl='\r\n' if '\r\n' in s else '\n'
def rep(a,b,c=1):
    global s
    a=a.replace('\n',nl); b=b.replace('\n',nl)
    assert s.count(a)==c,(a[:40],s.count(a)); s=s.replace(a,b)
rep("    struct Entry { std::string name; unsigned width, height, size; long offset; };\n    static std::vector<Entry> index;\n    static FILE* file = nullptr;",
    "    struct Entry { std::string name; unsigned width, height, size; long offset; FILE* file; };\n    static std::vector<Entry> index;")
rep("""        file = CatalogFile(L"EsteriaKvSkins.bin");
        unsigned head[2]{};
        if (file && std::fread(head, sizeof(head), 1, file) == 1 && head[0] == 0x3153564B)
        {
            for (unsigned i = 0; i < head[1]; ++i)
            {
                char header[144]{};
                if (std::fread(header, sizeof(header), 1, file) != 1)
                    break;
                Entry entry{std::string(header, strnlen(header, 128)), Field<unsigned>(header, 128), Field<unsigned>(header, 132),
                    Field<unsigned>(header, 136), std::ftell(file)};
                index.push_back(entry);
                if (std::fseek(file, static_cast<long>(entry.size), SEEK_CUR))
                    break;
            }
        }
""","""        for (wchar_t const* bank : {L"EsteriaKvSkins.bin", L"EsteriaPackSkins.bin"})      // the pack races' skins sit in their own bank
        {
            FILE* file = CatalogFile(bank);
            unsigned head[2]{};
            if (file && std::fread(head, sizeof(head), 1, file) == 1 && head[0] == 0x3153564B)
            {
                for (unsigned i = 0; i < head[1]; ++i)
                {
                    char header[144]{};
                    if (std::fread(header, sizeof(header), 1, file) != 1)
                        break;
                    Entry entry{std::string(header, strnlen(header, 128)), Field<unsigned>(header, 128), Field<unsigned>(header, 132),
                        Field<unsigned>(header, 136), std::ftell(file), file};
                    index.push_back(entry);
                    if (std::fseek(file, static_cast<long>(entry.size), SEEK_CUR))
                        break;
                }
            }
        }
""")
rep("if (!decompress || !file || !item.width","if (!decompress || !item.file || !item.width")
rep("if (std::fseek(file, item.offset, SEEK_SET) || std::fread(packed.data(), 1, packed.size(), file) != packed.size())","if (std::fseek(item.file, item.offset, SEEK_SET) || std::fread(packed.data(), 1, packed.size(), item.file) != packed.size())")
rep("        if (race == 77 || race == 78)\n        {\n            // pack races","        if (race == 77 || race == 78 || (race >= 79 && race <= 91))\n        {\n            // pack races")
s=s.rstrip()+nl+"""bool KvPackBind(void* character)
{
    unsigned race = RaceOf(CC<unsigned>(character, 0x18));
    if (race < 79 || race > 91)
        return true;
    return KvNativeBind(character, race, race == 79 ? 8u : CreatureAppearance::PackSkins[race - 80], 0, race == 84 || race == 85 || race == 91);
}
""".replace('\n',nl)
open(p,'w',encoding='utf-8',newline='').write(s)

p='HaranirMaterials.inl'; s=open(p,encoding='utf-8',newline='').read(); nl='\r\n' if '\r\n' in s else '\n'
rep("    if (RaceOf(CC<unsigned>(character, 0x18)) == 79 || CreatureAppearance::IsPack(RaceOf(CC<unsigned>(character, 0x18))))\n        return;       // plain colour skins from the selection bank",
    "    if (RaceOf(CC<unsigned>(character, 0x18)) == 79 || CreatureAppearance::IsPack(RaceOf(CC<unsigned>(character, 0x18))))\n    {\n        KvPackBind(character);       // plain colour skins from the selection bank, armor baked on top\n        return;\n    }")
open(p,'w',encoding='utf-8',newline='').write(s)

p='EsteriaAppearance.cpp'; s=open(p,encoding='utf-8',newline='').read(); nl='\r\n' if '\r\n' in s else '\n'
rep("            KvFacelessBind(character);\n        // Some source-hidden","            KvFacelessBind(character);\n        KvPackBind(character);\n        // Some source-hidden")
open(p,'w',encoding='utf-8',newline='').write(s)
print('ok')
