import { defineConfig } from 'vitepress'
import sidebarEn from './sidebars/en.mjs'
import sidebarZh from './sidebars/zh.mjs'

const base = process.env.BASE || '/'

export default defineConfig({
  title: 'Airalogy Masterbrain Docs',
  description: 'Bilingual documentation for Airalogy Masterbrain',
  base,
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    search: {
      provider: 'local'
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/airalogy/masterbrain' }]
  },
  locales: {
    en: {
      label: 'English',
      lang: 'en-US',
      link: '/en/',
      themeConfig: {
        nav: [{ text: 'GitHub', link: 'https://github.com/airalogy/masterbrain' }],
        sidebar: sidebarEn
      }
    },
    zh: {
      label: '中文',
      lang: 'zh-CN',
      link: '/zh/',
      themeConfig: {
        nav: [{ text: 'GitHub', link: 'https://github.com/airalogy/masterbrain' }],
        sidebar: sidebarZh
      }
    }
  }
})
