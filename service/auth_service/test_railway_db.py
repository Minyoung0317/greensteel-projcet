#!/usr/bin/env python3
"""
Railway PostgreSQL 회원가입 테이블 생성 및 테스트 스크립트
"""

import os
import sys
import asyncio
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError
import uuid
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.common.settings import settings
from app.common.db import Base, create_tables, test_database_connection
from app.domain.entities.company.company import Company
from app.domain.entities.user.user import User

def create_test_data():
    """테스트 데이터 생성"""
    
    # 1. 테스트 기업 데이터
    test_company = Company(
        uuid=str(uuid.uuid4()),
        company_id="test_company_001",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqQKqK",  # "password123"
        Installation="테스트 기업 (주)",
        Installation_en="Test Company Inc.",
        economic_activity="제조업",
        economic_activity_en="Manufacturing",
        representative="홍길동",
        representative_en="Hong Gil-dong",
        email="test@testcompany.com",
        telephone="02-1234-5678",
        street="테스트로",
        street_en="Test Street",
        number="123",
        number_en="123",
        postcode="12345",
        city="서울특별시",
        city_en="Seoul",
        country="대한민국",
        country_en="South Korea",
        unlocode="KR SEL",
        sourcelatitude=37.5665,
        sourcelongitude=126.9780
    )
    
    # 2. 테스트 사용자 데이터
    test_user = User(
        uuid=str(uuid.uuid4()),
        username="testuser",
        hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqQKqK",  # "password123"
        full_name="테스트 사용자",
        company_id=1,  # test_company의 ID
        role="admin",
        permissions='{"can_manage_users": true, "can_view_reports": true, "can_edit_data": true}',
        is_company_admin=True,
        can_manage_users=True,
        can_view_reports=True,
        can_edit_data=True,
        can_export_data=True,
        is_active=True
    )
    
    return test_company, test_user

def test_railway_postgresql():
    """Railway PostgreSQL 테스트"""
    
    print("🚀 Railway PostgreSQL 회원가입 테이블 테스트 시작")
    print("=" * 60)
    
    try:
        # 1. 데이터베이스 연결 테스트
        print("1️⃣ 데이터베이스 연결 테스트...")
        if not test_database_connection():
            print("❌ 데이터베이스 연결 실패")
            return False
        print("✅ 데이터베이스 연결 성공")
        
        # 2. 테이블 생성
        print("\n2️⃣ 테이블 생성...")
        create_tables()
        print("✅ 테이블 생성 완료")
        
        # 3. 생성된 테이블 확인
        print("\n3️⃣ 생성된 테이블 확인...")
        inspector = inspect(settings.engine)
        tables = inspector.get_table_names()
        print(f"📋 생성된 테이블: {tables}")
        
        # 4. 테이블 스키마 확인
        for table_name in tables:
            print(f"\n📊 {table_name} 테이블 스키마:")
            columns = inspector.get_columns(table_name)
            for column in columns:
                print(f"  - {column['name']}: {column['type']} (nullable: {column['nullable']})")
        
        # 5. 테스트 데이터 삽입
        print("\n4️⃣ 테스트 데이터 삽입...")
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=settings.engine)
        db = SessionLocal()
        
        try:
            # 기존 테스트 데이터 삭제 (중복 방지)
            db.query(User).filter(User.username == "testuser").delete()
            db.query(Company).filter(Company.company_id == "test_company_001").delete()
            db.commit()
            
            # 새 테스트 데이터 생성
            test_company, test_user = create_test_data()
            
            # 기업 데이터 삽입
            db.add(test_company)
            db.commit()
            db.refresh(test_company)
            print(f"✅ 기업 데이터 삽입 완료: {test_company.company_id}")
            
            # 사용자 데이터 삽입 (기업 ID 연결)
            test_user.company_id = test_company.id
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            print(f"✅ 사용자 데이터 삽입 완료: {test_user.username}")
            
            # 6. 데이터 조회 테스트
            print("\n5️⃣ 데이터 조회 테스트...")
            
            # 기업 조회
            company = db.query(Company).filter(Company.company_id == "test_company_001").first()
            if company:
                print(f"✅ 기업 조회 성공: {company.Installation}")
                print(f"   - 이메일: {company.email}")
                print(f"   - 주소: {company.city}, {company.country}")
            else:
                print("❌ 기업 조회 실패")
            
            # 사용자 조회
            user = db.query(User).filter(User.username == "testuser").first()
            if user:
                print(f"✅ 사용자 조회 성공: {user.full_name}")
                print(f"   - 역할: {user.role}")
                print(f"   - 기업 관리자: {user.is_company_admin}")
            else:
                print("❌ 사용자 조회 실패")
            
            # 관계 조회 테스트
            if user and user.company:
                print(f"✅ 관계 조회 성공: {user.username} → {user.company.Installation}")
            
            # 7. 회원가입 시나리오 테스트
            print("\n6️⃣ 회원가입 시나리오 테스트...")
            
            # 새 기업 등록
            new_company = Company(
                uuid=str(uuid.uuid4()),
                company_id="new_company_002",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqQKqK",
                Installation="새로운 기업 (주)",
                Installation_en="New Company Inc.",
                email="info@newcompany.com",
                telephone="02-9876-5432",
                city="부산광역시",
                country="대한민국"
            )
            
            db.add(new_company)
            db.commit()
            db.refresh(new_company)
            print(f"✅ 새 기업 등록: {new_company.Installation}")
            
            # 새 사용자 등록
            new_user = User(
                uuid=str(uuid.uuid4()),
                username="newuser",
                hashed_password="$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8KqQKqK",
                full_name="새로운 사용자",
                company_id=new_company.id,
                role="user",
                is_company_admin=False,
                is_active=True
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            print(f"✅ 새 사용자 등록: {new_user.full_name}")
            
            # 8. 최종 데이터 확인
            print("\n7️⃣ 최종 데이터 확인...")
            total_companies = db.query(Company).count()
            total_users = db.query(User).count()
            print(f"📊 총 기업 수: {total_companies}")
            print(f"📊 총 사용자 수: {total_users}")
            
            print("\n🎉 Railway PostgreSQL 회원가입 테스트 완료!")
            print("=" * 60)
            
            return True
            
        except Exception as e:
            print(f"❌ 테스트 데이터 처리 중 오류: {str(e)}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Railway PostgreSQL 테스트 실패: {str(e)}")
        return False

def main():
    """메인 함수"""
    print("🔧 Railway PostgreSQL 회원가입 시스템 테스트")
    print("=" * 60)
    
    # 환경변수 확인
    print("📋 환경변수 확인:")
    print(f"   - DATABASE_URL: {'설정됨' if settings.DATABASE_URL else '설정되지 않음'}")
    print(f"   - DATABASE_SSL_MODE: {settings.DATABASE_SSL_MODE}")
    print(f"   - SERVICE_NAME: {settings.SERVICE_NAME}")
    
    if not settings.DATABASE_URL:
        print("❌ DATABASE_URL이 설정되지 않았습니다.")
        print("   Railway에서 PostgreSQL 서비스의 연결 정보를 확인하세요.")
        return
    
    # 테스트 실행
    success = test_railway_postgresql()
    
    if success:
        print("\n✅ 모든 테스트가 성공적으로 완료되었습니다!")
        print("🚀 이제 auth-service를 Railway에 배포할 수 있습니다.")
    else:
        print("\n❌ 테스트 중 오류가 발생했습니다.")
        print("🔧 환경변수와 데이터베이스 연결을 확인하세요.")

if __name__ == "__main__":
    main()
