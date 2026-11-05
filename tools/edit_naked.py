p='KvOutfits.inl'; s=open(p,encoding='utf-8',newline='').read(); nl='\r\n' if '\r\n' in s else '\n'
def rep(a,b):
    global s
    a=a.replace('\n',nl); b=b.replace('\n',nl); assert s.count(a)==1,a[:50]; s=s.replace(a,b)
rep("    auto const* skin = skinPath ? KvSkin(skinPath) : nullptr;\n    auto const* map = KvMap(race, gender);",
"""    // pack races: the body skin with its painted-on gear inpainted, laid under the armor (copied: the skin cache may be cleared by the next lookup)
    std::vector<unsigned char> nakedPixels;
    unsigned nakedWidth = 0, nakedHeight = 0;
    if (skinPath && race >= 79 && race <= 91)
        if (auto const* naked = KvSkin((std::string("naked\\\\") + skinPath).c_str()))
        {
            nakedPixels = naked->rgba;
            nakedWidth = naked->width;
            nakedHeight = naked->height;
        }
    auto const* skin = skinPath ? KvSkin(skinPath) : nullptr;
    auto const* map = KvMap(race, gender);""")
rep("            unsigned char pixel[4];\n            for (int c = 0; c < 3; ++c)\n                pixel[c] = static_cast<unsigned char>((std::min)(255.0f, layer[4 * i + c] / a + 0.5f));\n            pixel[3] = static_cast<unsigned char>((std::min)(255.0f, a * 255.0f + 0.5f));\n            KvOver(body.data() + 4 * i, pixel);",
"""            unsigned char pixel[4];
            for (int c = 0; c < 3; ++c)
                pixel[c] = static_cast<unsigned char>((std::min)(255.0f, layer[4 * i + c] / a + 0.5f));
            pixel[3] = static_cast<unsigned char>((std::min)(255.0f, a * 255.0f + 0.5f));
            if (nakedWidth == map->width && nakedHeight == map->height && a > 0.5f)
                std::memcpy(body.data() + 4 * i, nakedPixels.data() + 4 * i, 4);
            KvOver(body.data() + 4 * i, pixel);""")
open(p,'w',encoding='utf-8',newline='').write(s); print('ok')
