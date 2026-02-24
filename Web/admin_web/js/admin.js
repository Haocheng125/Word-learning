// API 配置
const API_BASE_URL = 'http://localhost:8080/api';

// 当前登录状态
let isLoggedIn = false;

// 页面加载完成
document.addEventListener('DOMContentLoaded', function() {
    // 登录表单
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', handleLogin);

    // 退出登录
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);

    // 导航切换
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', handleNavClick);
    });

    // 关于我们表单
    document.getElementById('aboutForm').addEventListener('submit', handleAboutSubmit);

    // 联系我们表单
    document.getElementById('contactForm').addEventListener('submit', handleContactSubmit);

    // 产品与服务
    document.getElementById('addProductBtn').addEventListener('click', () => openProductModal());
    document.getElementById('productForm').addEventListener('submit', handleProductSubmit);

    // 成功案例
    document.getElementById('addCaseBtn').addEventListener('click', () => openCaseModal());
    document.getElementById('caseForm').addEventListener('submit', handleCaseSubmit);

    // 弹窗关闭
    document.querySelectorAll('.modal .close').forEach(close => {
        close.addEventListener('click', closeAllModals);
    });
});

// 登录处理
async function handleLogin(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/admin/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const result = await response.json();
        
        if (result.success) {
            isLoggedIn = true;
            document.getElementById('loginPage').style.display = 'none';
            document.getElementById('adminPage').style.display = 'flex';
            loadAboutData();
            alert('登录成功！');
        } else {
            alert(result.message || '登录失败');
        }
    } catch (error) {
        console.error('登录错误:', error);
        alert('登录失败，请检查服务器连接');
    }
}

// 退出登录
function handleLogout() {
    isLoggedIn = false;
    document.getElementById('adminPage').style.display = 'none';
    document.getElementById('loginPage').style.display = 'flex';
    document.getElementById('loginForm').reset();
}

// 导航切换
function handleNavClick(e) {
    e.preventDefault();
    const page = e.target.dataset.page;

    // 更新导航激活状态
    document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
    e.target.classList.add('active');

    // 更新内容页面
    document.querySelectorAll('.content-page').forEach(page => page.classList.remove('active'));
    document.getElementById(`${page}Page`).classList.add('active');

    // 加载对应数据
    switch(page) {
        case 'about':
            loadAboutData();
            break;
        case 'contact':
            loadContactData();
            break;
        case 'products':
            loadProductsData();
            break;
        case 'cases':
            loadCasesData();
            break;
        case 'consultations':
            loadConsultationsData();
            break;
    }
}

// 加载关于我们数据
async function loadAboutData() {
    try {
        const response = await fetch(`${API_BASE_URL}/about`);
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            document.getElementById('about_id').value = data.id || '';
            document.getElementById('about_title').value = data.title || '';
            document.getElementById('about_content').value = data.content || '';
            document.getElementById('about_stat1Label').value = data.stat1Label || '';
            document.getElementById('about_stat1Value').value = data.stat1Value || '';
            document.getElementById('about_stat2Label').value = data.stat2Label || '';
            document.getElementById('about_stat2Value').value = data.stat2Value || '';
            document.getElementById('about_stat3Label').value = data.stat3Label || '';
            document.getElementById('about_stat3Value').value = data.stat3Value || '';
            document.getElementById('about_imageUrl').value = data.imageUrl || '';
        }
    } catch (error) {
        console.error('加载关于我们数据失败:', error);
    }
}

// 保存关于我们
async function handleAboutSubmit(e) {
    e.preventDefault();
    
    const data = {
        id: document.getElementById('about_id').value || null,
        title: document.getElementById('about_title').value,
        content: document.getElementById('about_content').value,
        stat1Label: document.getElementById('about_stat1Label').value,
        stat1Value: document.getElementById('about_stat1Value').value,
        stat2Label: document.getElementById('about_stat2Label').value,
        stat2Value: document.getElementById('about_stat2Value').value,
        stat3Label: document.getElementById('about_stat3Label').value,
        stat3Value: document.getElementById('about_stat3Value').value,
        imageUrl: document.getElementById('about_imageUrl').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/about`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (result.success) {
            alert('保存成功！');
            loadAboutData();
        } else {
            alert('保存失败：' + result.message);
        }
    } catch (error) {
        console.error('保存失败:', error);
        alert('保存失败，请稍后重试');
    }
}

// 加载联系我们数据
async function loadContactData() {
    try {
        const response = await fetch(`${API_BASE_URL}/contact`);
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            document.getElementById('contact_id').value = data.id || '';
            document.getElementById('contact_address').value = data.address || '';
            document.getElementById('contact_phone').value = data.phone || '';
            document.getElementById('contact_email').value = data.email || '';
            document.getElementById('contact_workingHours').value = data.workingHours || '';
        }
    } catch (error) {
        console.error('加载联系我们数据失败:', error);
    }
}

// 保存联系我们
async function handleContactSubmit(e) {
    e.preventDefault();
    
    const data = {
        id: document.getElementById('contact_id').value || null,
        address: document.getElementById('contact_address').value,
        phone: document.getElementById('contact_phone').value,
        email: document.getElementById('contact_email').value,
        workingHours: document.getElementById('contact_workingHours').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (result.success) {
            alert('保存成功！');
            loadContactData();
        } else {
            alert('保存失败：' + result.message);
        }
    } catch (error) {
        console.error('保存失败:', error);
        alert('保存失败，请稍后重试');
    }
}

// 加载产品列表
async function loadProductsData() {
    try {
        const response = await fetch(`${API_BASE_URL}/products`);
        const result = await response.json();
        
        if (result.success) {
            const products = result.data || [];
            const listEl = document.getElementById('productsList');
            
            listEl.innerHTML = products.map(product => `
                <div class="item-card">
                    <div class="item-header">
                        <div>
                            <h3>${product.icon || ''} ${product.title}</h3>
                            <span class="item-tag">顺序: ${product.displayOrder}</span>
                        </div>
                        <div class="item-actions">
                            <button class="btn-edit" onclick="editProduct(${product.id})">编辑</button>
                            <button class="btn-delete" onclick="deleteProduct(${product.id})">删除</button>
                        </div>
                    </div>
                    <div class="item-content">${product.description}</div>
                    ${product.imageUrl ? `<div class="item-meta"><span>图片: ${product.imageUrl}</span></div>` : ''}
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('加载产品列表失败:', error);
    }
}

// 打开产品弹窗
function openProductModal(id = null) {
    const modal = document.getElementById('productModal');
    const form = document.getElementById('productForm');
    
    if (id) {
        document.getElementById('productModalTitle').textContent = '编辑产品';
        loadProductDetail(id);
    } else {
        document.getElementById('productModalTitle').textContent = '添加产品';
        form.reset();
        document.getElementById('product_id').value = '';
    }
    
    modal.classList.add('active');
}

// 加载产品详情
async function loadProductDetail(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${id}`);
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            document.getElementById('product_id').value = data.id;
            document.getElementById('product_title').value = data.title || '';
            document.getElementById('product_icon').value = data.icon || '';
            document.getElementById('product_description').value = data.description || '';
            document.getElementById('product_imageUrl').value = data.imageUrl || '';
            document.getElementById('product_features').value = data.features || '';
            document.getElementById('product_displayOrder').value = data.displayOrder || 0;
        }
    } catch (error) {
        console.error('加载产品详情失败:', error);
    }
}

// 编辑产品
function editProduct(id) {
    openProductModal(id);
}

// 删除产品
async function deleteProduct(id) {
    if (!confirm('确定要删除这个产品吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/products/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            alert('删除成功！');
            loadProductsData();
        } else {
            alert('删除失败：' + result.message);
        }
    } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败，请稍后重试');
    }
}

// 保存产品
async function handleProductSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('product_id').value;
    const data = {
        title: document.getElementById('product_title').value,
        icon: document.getElementById('product_icon').value,
        description: document.getElementById('product_description').value,
        imageUrl: document.getElementById('product_imageUrl').value,
        features: document.getElementById('product_features').value,
        displayOrder: parseInt(document.getElementById('product_displayOrder').value) || 0
    };

    try {
        const url = id ? `${API_BASE_URL}/products/${id}` : `${API_BASE_URL}/products`;
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (result.success) {
            alert('保存成功！');
            closeAllModals();
            loadProductsData();
        } else {
            alert('保存失败：' + result.message);
        }
    } catch (error) {
        console.error('保存失败:', error);
        alert('保存失败，请稍后重试');
    }
}

// 加载案例列表
async function loadCasesData() {
    try {
        const response = await fetch(`${API_BASE_URL}/cases`);
        const result = await response.json();
        
        if (result.success) {
            const cases = result.data || [];
            const listEl = document.getElementById('casesList');
            
            listEl.innerHTML = cases.map(c => `
                <div class="item-card">
                    <div class="item-header">
                        <div>
                            <h3>${c.title}</h3>
                            <span class="item-tag">${c.category || '未分类'}</span>
                            <span class="item-tag">顺序: ${c.displayOrder}</span>
                        </div>
                        <div class="item-actions">
                            <button class="btn-edit" onclick="editCase(${c.id})">编辑</button>
                            <button class="btn-delete" onclick="deleteCase(${c.id})">删除</button>
                        </div>
                    </div>
                    <div class="item-content">${c.description}</div>
                    <div class="item-meta">
                        ${c.result1Label ? `<span>${c.result1Label}: ${c.result1Value}</span>` : ''}
                        ${c.result2Label ? `<span>${c.result2Label}: ${c.result2Value}</span>` : ''}
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('加载案例列表失败:', error);
    }
}

// 打开案例弹窗
function openCaseModal(id = null) {
    const modal = document.getElementById('caseModal');
    const form = document.getElementById('caseForm');
    
    if (id) {
        document.getElementById('caseModalTitle').textContent = '编辑案例';
        loadCaseDetail(id);
    } else {
        document.getElementById('caseModalTitle').textContent = '添加案例';
        form.reset();
        document.getElementById('case_id').value = '';
    }
    
    modal.classList.add('active');
}

// 加载案例详情
async function loadCaseDetail(id) {
    try {
        const response = await fetch(`${API_BASE_URL}/cases/${id}`);
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            document.getElementById('case_id').value = data.id;
            document.getElementById('case_title').value = data.title || '';
            document.getElementById('case_category').value = data.category || '';
            document.getElementById('case_description').value = data.description || '';
            document.getElementById('case_imageUrl').value = data.imageUrl || '';
            document.getElementById('case_result1Label').value = data.result1Label || '';
            document.getElementById('case_result1Value').value = data.result1Value || '';
            document.getElementById('case_result2Label').value = data.result2Label || '';
            document.getElementById('case_result2Value').value = data.result2Value || '';
            document.getElementById('case_displayOrder').value = data.displayOrder || 0;
        }
    } catch (error) {
        console.error('加载案例详情失败:', error);
    }
}

// 编辑案例
function editCase(id) {
    openCaseModal(id);
}

// 删除案例
async function deleteCase(id) {
    if (!confirm('确定要删除这个案例吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/cases/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            alert('删除成功！');
            loadCasesData();
        } else {
            alert('删除失败：' + result.message);
        }
    } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败，请稍后重试');
    }
}

// 保存案例
async function handleCaseSubmit(e) {
    e.preventDefault();
    
    const id = document.getElementById('case_id').value;
    const data = {
        title: document.getElementById('case_title').value,
        category: document.getElementById('case_category').value,
        description: document.getElementById('case_description').value,
        imageUrl: document.getElementById('case_imageUrl').value,
        result1Label: document.getElementById('case_result1Label').value,
        result1Value: document.getElementById('case_result1Value').value,
        result2Label: document.getElementById('case_result2Label').value,
        result2Value: document.getElementById('case_result2Value').value,
        displayOrder: parseInt(document.getElementById('case_displayOrder').value) || 0
    };

    try {
        const url = id ? `${API_BASE_URL}/cases/${id}` : `${API_BASE_URL}/cases`;
        const method = id ? 'PUT' : 'POST';
        
        const response = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json();
        
        if (result.success) {
            alert('保存成功！');
            closeAllModals();
            loadCasesData();
        } else {
            alert('保存失败：' + result.message);
        }
    } catch (error) {
        console.error('保存失败:', error);
        alert('保存失败，请稍后重试');
    }
}

// 加载用户咨询列表
async function loadConsultationsData() {
    try {
        const response = await fetch(`${API_BASE_URL}/consultations`);
        const result = await response.json();
        
        if (result.success) {
            const consultations = result.data || [];
            const listEl = document.getElementById('consultationsList');
            
            listEl.innerHTML = consultations.map(c => `
                <div class="item-card">
                    <div class="item-header">
                        <div>
                            <h3>${c.name} - ${c.company || '未填写公司'}</h3>
                        </div>
                        <div class="item-actions">
                            <button class="btn-delete" onclick="deleteConsultation(${c.id})">删除</button>
                        </div>
                    </div>
                    <div class="item-content">${c.content}</div>
                    <div class="item-meta">
                        ${c.phone ? `<span>电话: ${c.phone}</span>` : ''}
                        ${c.email ? `<span>邮箱: ${c.email}</span>` : ''}
                        <span>时间: ${new Date(c.createdAt).toLocaleString('zh-CN')}</span>
                    </div>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('加载咨询列表失败:', error);
    }
}

// 删除咨询
async function deleteConsultation(id) {
    if (!confirm('确定要删除这条咨询记录吗？')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/consultations/${id}`, {
            method: 'DELETE'
        });

        const result = await response.json();
        
        if (result.success) {
            alert('删除成功！');
            loadConsultationsData();
        } else {
            alert('删除失败：' + result.message);
        }
    } catch (error) {
        console.error('删除失败:', error);
        alert('删除失败，请稍后重试');
    }
}

// 关闭所有弹窗
function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('active');
    });
}
