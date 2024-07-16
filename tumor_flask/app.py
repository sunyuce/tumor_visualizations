import os

from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# 配置 MySQL 数据库连接
db_config = {
    'user': 'root',
    'password': '32101151',
    'host': 'localhost',
    'database': 'tumor',
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 获取查询参数
    patient_number = request.args.get('patient_number', '')
    gender = request.args.get('gender', '')
    survival_status = request.args.get('survival_status', '')
    page = int(request.args.get('page', 1))
    limit = 10
    offset = (page - 1) * limit

    # 构建查询语句
    query = "SELECT * FROM patients WHERE 1=1"
    count_query = "SELECT COUNT(*) as count FROM patients WHERE 1=1"
    params = []
    count_params = []

    if patient_number:
        query += " AND Patient LIKE %s"
        count_query += " AND Patient LIKE %s"
        params.append(f"%{patient_number}%")
        count_params.append(f"%{patient_number}%")
    if gender:
        query += " AND gender = %s"
        count_query += " AND gender = %s"
        params.append(gender)
        count_params.append(gender)
    if survival_status:
        query += " AND death01 = %s"
        count_query += " AND death01 = %s"
        params.append(survival_status)
        count_params.append(survival_status)

    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    patients = cursor.fetchall()

    # 获取总记录数用于分页
    cursor.execute(count_query, tuple(count_params))
    total_records = cursor.fetchone()['count']
    total_pages = (total_records + limit - 1) // limit

    cursor.close()
    conn.close()

    return render_template('index.html', patients=patients, page=page, total_pages=total_pages,
                           patient_number=patient_number, gender=gender, survival_status=survival_status)

@app.route('/patient/<int:patient_id>', methods=['GET'])
def patient_detail(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
    patient = cursor.fetchone()

    cursor.close()
    conn.close()

    if patient:
        patient_number = patient['Patient']
        image_folder = os.path.join('static/brain_origin', str(patient_number))
        num_images = len(
            [name for name in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, name))])
        return render_template('patient_detail.html', patient=patient, num_images=num_images)
    else:
        return "Patient not found", 404

if __name__ == '__main__':
    app.run(debug=True)
