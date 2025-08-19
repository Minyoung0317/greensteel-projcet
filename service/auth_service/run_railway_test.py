#!/usr/bin/env python3
"""
Railway PostgreSQL 테스트 실행 스크립트
"""

import os
import sys
import subprocess

def run_test():
    """테스트 실행"""
    print("🚀 Railway PostgreSQL 회원가입 테이블 테스트 실행")
    print("=" * 60)
    
    # 현재 디렉토리를 auth_service로 변경
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 환경변수 확인
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL 환경변수가 설정되지 않았습니다.")
        print("🔧 Railway에서 PostgreSQL 연결 정보를 확인하세요.")
        return False
    
    print(f"✅ DATABASE_URL: {database_url.split('@')[1] if '@' in database_url else '설정됨'}")
    
    try:
        # 테스트 스크립트 실행
        result = subprocess.run([
            sys.executable, 
            'test_railway_db.py'
        ], capture_output=True, text=True, cwd=os.getcwd())
        
        # 결과 출력
        print(result.stdout)
        if result.stderr:
            print("⚠️ 경고/오류:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 테스트 실행 중 오류: {str(e)}")
        return False

def main():
    """메인 함수"""
    success = run_test()
    
    if success:
        print("\n🎉 테스트가 성공적으로 완료되었습니다!")
        print("✅ Railway PostgreSQL이 회원가입 시스템에 적합합니다.")
    else:
        print("\n❌ 테스트가 실패했습니다.")
        print("🔧 환경변수와 데이터베이스 연결을 확인하세요.")

if __name__ == "__main__":
    main()
