from ArticleFinder import ArticleFinder

a = ArticleFinder('https://mediabiasfactcheck.com/pro-science/')
b = ArticleFinder('https://mediabiasfactcheck.com/conspiracy/')

print(a.articles)
print(b.articles)
