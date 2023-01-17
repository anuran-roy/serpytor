# The SerPytor Docs
  
A distributed, low-code, end-to-end data collection and analysis tool for data folks. Take the pain out of data collection from your pipeline!  

***NOTE***: PLEASE DON'T USE IT IN PRODUCTION YET!

[![Codacy Security Scan](https://github.com/anuran-roy/serpytor/actions/workflows/codacy.yml/badge.svg?branch=main)](https://github.com/anuran-roy/serpytor/actions/workflows/codacy.yml)

[![CodeQL](https://github.com/anuran-roy/serpytor/actions/workflows/codeql.yml/badge.svg?branch=main)](https://github.com/anuran-roy/serpytor/actions/workflows/codeql.yml)

[![Docs](https://github.com/anuran-roy/serpytor/actions/workflows/pages/pages-build-deployment/badge.svg?branch=main)](https://github.com/anuran-roy/serpytor/actions/workflows/pages/pages-build-deployment)

## Where did it come from?
  
Alright, I'll be completely honest here. It's a story, so if you're in, read along! Busy folks, the [TL;DR](#tl-dr) is for you!  
  
### The Story
  
I was always fascinated by large-scale system design and big data pipelines - on the scale of billions. Statistics released from time to time by companies like AWS, Google, Cloudflare and others intensified my fascination further.  
  
I read a lot of newsletters, blogs and articles about how to implement large scale system design, I still do. But it always felt like an enigma - something that is not as easy as the online resources make it to be. Special mention to Alex Xu's newsletters and his gem of a book on System Design Interview (I've read only the first part, eagerly waiting for the second to arrive 😃)  
  
Fast forward to my summer holidays, I decided that something needs to be done, else I'll remain stuck in this loop of getting hyped and feeling inadequate.

**Then came a twist.**  
  
As I kept working and learning, I came to know about the so-called *Modern Data Stack* and how many experts claimed that the way is not sustainable in anyway imaginable. Especially one point stuck me from a newsletter (sorry I don't remember the name) that proposed a solution for the disparity and the inconvenience caused by the hugely heterogeneous nature of the Modern Data Stack. It was to homogenise the different heterogeneous components, such that components logically connected to each other are implemented into a homogeneous layer. I interpreted it as:
  
> Connect wherever possible; segregate wherever required.

I was also inspired by the way the people at [**naas.ai**](https://naas.ai) do their work:

- First they build the core, low-level drivers
- Then their contributors build a low-code platform (I happen to be one of them 😃) by creating templates on top of the drivers
- Then they let their consumers build services using those templates.

This brought me to the conclusion - Moving data quick needs to be of three-levels, not the one-stop solution many products claim to be. Yes, they may do a lot of things correct, but because of the unlimited variety in data, there might be cases where the so-called one-stop solution falls short.

Thus, I started this project. I could never guess that the codebase would grow so much so quickly!  
  
### TL; DR

This project was taken up by me as a challenge to understand big data architecture, and to find a low-code unified alternative to the plethora of conflicting data products out there. It's been quite a journey till now!  
  
## Why Open Source this?

There are mainly two reasons:

- **Learning Large-scale System Design while doing it**: System Design is one of the most sought-after skills in the software industry, and I know for sure that I am not the only one stuck in the vicious loop of feeling there is some black magic, trying to learn it, and end up feeling inadequate to learn the stuff.  
I am someone who learns by doing. So I wanted to make something tangible to start off with.  
  
- ***The more important reason-* A modest attempt at a unified data platform**: I've been thoroughly confused about the different tools that exist in the Big Data Space - and a lot of them have almost same functionalities, if not exactly the same. It's okay to do one thing and do it good, but somewhere down the line, I think that so many options to choose from gives rise to a lot of confusion. For example, considering data formats, there are many conflicts, due to which many other extra software also needs to be introduced.  

## Getting Started

Getting started with SerPyTor is extremely easy. You can use it as a library, framework, and/or as a service (under development).

Install SerPyTor with the following two steps:

- Clone the Git Repo on your local machine and navigate into it:

```sh
git clone https://github.com/anuran-roy/serpytor.git
cd serpytor
```

- Run `pip install`:

```sh
pip install .
```

## SerPyTor Architecture

As I mentioned before, SerPyTor is being created in a way that it can act as a library, framework, and/or as a service. Hence, there are three main parts of SerPyTor:

1. **SerPyTor Components**: The building blocks of SerPyTor. These are the most fundamental components of SerPyTor, and are used by the SerPyTor Framework and the SerPyTor Services.  

2. **SerPyTor Framework**: This is to aid developers ship code faster, and in a consistent fashion, in ways that make best use of the capabilities that SerPyTor provides. If you want something pre-made and ready to ship in no time (viz., templates), this is what you want to check out.

3. **SerPyTor Services**: SerPyTor services are meant for quick and effortless deployment and integration of SerPyTor-based code and products.
  
As of now (October, 2022), I am dedicating my efforts towards building a diverse set of SerPyTor components that can be used to create a robust framework.

## Contributing to SerPyTor

Contributors are the driving force behind an open-source project, and SerPyTor aims to be 100% open source in nature! As a big fan of open source projects, anyone willing to lend me a helping hand in growing this project is most welcome! 🤩

You can talk in Discussions, create Issues and Pull Requests in the [**GitHub repository**](https://github.com/anuran-roy/serpytor), or mail me directly at anuranroy02 [at] gmail.com 😃
