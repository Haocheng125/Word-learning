// API调用封装
class API {
    static async request(url, options = {}) {
        try {
            const response = await fetch(API_BASE_URL + url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });
            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    static async getAboutUs() {
        return this.request(API_ENDPOINTS.ABOUT);
    }

    static async getContactInfo() {
        return this.request(API_ENDPOINTS.CONTACT);
    }

    static async getProductServices() {
        return this.request(API_ENDPOINTS.PRODUCTS);
    }

    static async getSuccessCases() {
        return this.request(API_ENDPOINTS.CASES);
    }

    static async submitConsultation(data) {
        return this.request(API_ENDPOINTS.CONSULTATION, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
}

// 页面加载后获取数据并渲染
document.addEventListener('DOMContentLoaded', async function() {
    console.log('开始加载数据...');
    
    try {
        // 加载关于我们数据
        await loadAboutUs();
        
        // 加载联系我们数据
        await loadContactInfo();
        
        // 加载产品与服务数据
        await loadProductServices();
        
        // 加载成功案例数据
        await loadSuccessCases();
    } catch (error) {
        console.error('加载页面数据失败:', error);
    }
    
    // 表单提交处理
    const form = document.querySelector('.contact-form');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const data = {
                name: form.querySelector('input[type="text"]').value,
                phone: form.querySelector('input[type="tel"]').value,
                email: form.querySelector('input[type="email"]').value,
                company: form.querySelectorAll('input[type="text"]')[1].value,
                content: form.querySelector('textarea').value
            };
            
            try {
                const result = await API.submitConsultation(data);
                if (result.success) {
                    alert('提交成功！我们会尽快与您联系。');
                    form.reset();
                } else {
                    alert('提交失败：' + result.message);
                }
            } catch (error) {
                alert('提交失败，请稍后重试');
            }
        });
    }
});

// 加载关于我们数据
async function loadAboutUs() {
    try {
        const result = await API.getAboutUs();
        if (result.success && result.data) {
            const data = result.data;
            
            // 更新标题和内容
            const aboutContent = document.querySelector('.about-content h3');
            if (aboutContent && data.title) {
                aboutContent.innerHTML = data.title;
            }
            
            const aboutText = document.querySelector('.about-content p');
            if (aboutText && data.content) {
                aboutText.textContent = data.content;
            }
            
            // 更新统计数据
            const stats = document.querySelectorAll('.stat-item');
            if (stats.length >= 3) {
                if (data.stat1Value) {
                    stats[0].querySelector('.stat-number').textContent = data.stat1Value;
                    stats[0].querySelector('.stat-label').textContent = data.stat1Label || '';
                }
                if (data.stat2Value) {
                    stats[1].querySelector('.stat-number').textContent = data.stat2Value;
                    stats[1].querySelector('.stat-label').textContent = data.stat2Label || '';
                }
                if (data.stat3Value) {
                    stats[2].querySelector('.stat-number').textContent = data.stat3Value;
                    stats[2].querySelector('.stat-label').textContent = data.stat3Label || '';
                }
            }
        }
    } catch (error) {
        console.error('加载关于我们数据失败:', error);
    }
}

// 加载联系我们数据
async function loadContactInfo() {
    try {
        const result = await API.getContactInfo();
        if (result.success && result.data) {
            const data = result.data;
            const contactDetails = document.querySelectorAll('.contact-details li');
            
            if (contactDetails.length >= 4) {
                // 更新地址
                if (data.address) {
                    contactDetails[0].querySelector('.contact-text span').textContent = data.address;
                }
                // 更新电话
                if (data.phone) {
                    contactDetails[1].querySelector('.contact-text span').textContent = data.phone;
                }
                // 更新邮箱
                if (data.email) {
                    contactDetails[2].querySelector('.contact-text span').textContent = data.email;
                }
                // 更新工作时间
                if (data.workingHours) {
                    contactDetails[3].querySelector('.contact-text span').textContent = data.workingHours;
                }
            }
        }
    } catch (error) {
        console.error('加载联系我们数据失败:', error);
    }
}

// 加载产品与服务数据
async function loadProductServices() {
    try {
        const result = await API.getProductServices();
        if (result.success && result.data && result.data.length > 0) {
            const products = result.data;
            const servicesGrid = document.querySelector('.services-grid');
            
            if (servicesGrid) {
                servicesGrid.innerHTML = products.map(product => `
                    <div class="service-card">
                        ${product.imageUrl ? `<img src="${product.imageUrl}" alt="${product.title}">` : ''}
                        <div class="service-icon">${product.icon || '🔧'}</div>
                        <h4>${product.title}</h4>
                        <p>${product.description || ''}</p>
                        ${product.features ? `
                            <ul class="service-features">
                                ${product.features.split('\n').filter(f => f.trim()).map(feature => 
                                    `<li>${feature.trim()}</li>`
                                ).join('')}
                            </ul>
                        ` : ''}
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('加载产品与服务数据失败:', error);
    }
}

// 加载成功案例数据
async function loadSuccessCases() {
    try {
        const result = await API.getSuccessCases();
        if (result.success && result.data && result.data.length > 0) {
            const cases = result.data;
            const casesGrid = document.querySelector('.cases-grid');
            
            if (casesGrid) {
                casesGrid.innerHTML = cases.map(c => `
                    <div class="case-card">
                        <div class="case-image">
                            ${c.imageUrl ? `<img src="${c.imageUrl}" alt="${c.title}">` : ''}
                            <div class="case-overlay"></div>
                            ${c.category ? `<span class="case-tag">${c.category}</span>` : ''}
                        </div>
                        <div class="case-content">
                            <h4>${c.title}</h4>
                            <p>${c.description || ''}</p>
                            <div class="case-results">
                                ${c.result1Value ? `
                                    <div class="result-item">
                                        <div class="result-value">${c.result1Value}</div>
                                        <div class="result-label">${c.result1Label || ''}</div>
                                    </div>
                                ` : ''}
                                ${c.result2Value ? `
                                    <div class="result-item">
                                        <div class="result-value">${c.result2Value}</div>
                                        <div class="result-label">${c.result2Label || ''}</div>
                                    </div>
                                ` : ''}
                            </div>
                        </div>
                    </div>
                `).join('');
            }
        }
    } catch (error) {
        console.error('加载成功案例数据失败:', error);
    }
}
