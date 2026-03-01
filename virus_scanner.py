import os
import platform
import subprocess
import aiofiles
from typing import Dict, Any


async def basic_scan(file_path: str) -> Dict[str, Any]:
    """
    Asosiy tekshirish (agar ClamAV bo'lmasa)
    - Xavfli kengaytmalarni tekshiradi
    - Fayl hajmini tekshiradi
    - Fayl boshidagi magic bytes ni tekshiradi
    """
    dangerous_extensions = [
        '.exe', '.bat', '.cmd', '.vbs', '.ps1',
        '.jar', '.js', '.jse', '.wsf', '.wsh',
        '.msi', '.msp', '.mst', '.hta', '.cpl',
        '.scr', '.pif', '.application', '.gadget',
        '.msc', '.vb', '.vbe', '.ws', '.wsc',
        '.ps2', '.ps1xml', '.ps2xml', '.psc1',
        '.psc2', '.msh', '.msh1', '.msh2', '.mshxml',
        '.msh1xml', '.msh2xml', '.scf', '.lnk', '.inf'
    ]

    # Fayl nomini olish
    file_name = os.path.basename(file_path).lower()

    # Xavfli kengaytmalarni tekshirish
    file_ext = os.path.splitext(file_name)[1].lower()
    if file_ext in dangerous_extensions:
        return {
            'is_infected': True,
            'virus_name': f'Xavfli kengaytma: {file_ext}',
            'scanner': 'basic',
            'reason': 'dangerous_extension'
        }

    # Fayl hajmini tekshirish (50MB dan katta)
    file_size = os.path.getsize(file_path)
    if file_size > 50 * 1024 * 1024:  # 50MB
        return {
            'is_infected': True,
            'virus_name': 'Fayl hajmi juda katta (50MB+)',
            'scanner': 'basic',
            'reason': 'file_too_large'
        }

    # Fayl boshidagi magic bytes ni tekshirish (double extension)
    try:
        async with aiofiles.open(file_path, 'rb') as f:
            header = await f.read(4)

        # PDF fayl
        if file_ext == '.pdf' and header != b'%PDF':
            return {
                'is_infected': True,
                'virus_name': 'Soxta PDF fayl',
                'scanner': 'basic',
                'reason': 'fake_pdf'
            }

        # ZIP arxiv
        if file_ext in ['.zip', '.jar'] and header[:2] != b'PK':
            return {
                'is_infected': True,
                'virus_name': 'Soxta arxiv fayl',
                'scanner': 'basic',
                'reason': 'fake_archive'
            }

    except:
        pass

    return {
        'is_infected': False,
        'scanner': 'basic',
        'file_name': file_name,
        'file_size': file_size
    }


def extract_virus_name(clamav_output: str) -> str:
    """ClamAV outputdan virus nomini ajratib olish"""
    try:
        for line in clamav_output.split('\n'):
            if 'FOUND' in line:
                parts = line.split(':')
                if len(parts) > 1:
                    return parts[1].strip().replace('FOUND', '').strip()
    except:
        pass
    return "Noma'lum virus"


class VirusScanner:
    def __init__(self):
        self.clamav_path = None
        self.system = platform.system()
        self.clamav_available = self.check_clamav()

    def check_clamav(self):
        """ClamAV mavjudligini tekshirish"""
        try:
            if self.system == "Windows":
                # Windows uchun ClamAV yo'llari
                possible_paths = [
                    r"C:\Program Files\ClamAV\clamscan.exe",
                    r"C:\Program Files (x86)\ClamAV\clamscan.exe",
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        self.clamav_path = path
                        return True
            else:
                # Linux/Mac uchun
                result = subprocess.run(['which', 'clamscan'], capture_output=True)
                if result.returncode == 0:
                    self.clamav_path = 'clamscan'
                    return True
        except:
            pass

        print("⚠️ ClamAV topilmadi. Asosiy tekshirish rejimi ishlaydi.")
        return False

    async def scan_file(self, file_path: str) -> Dict[str, Any]:
        """
        Faylni virusga tekshirish
        """
        try:
            if self.clamav_available:
                # ClamAV orqali tekshirish
                return await self.scan_with_clamav(file_path)
            else:
                # Asosiy tekshirish
                return await basic_scan(file_path)
        except Exception as e:
            print(f"Virus tekshirishda xatolik: {e}")
            return {
                'is_infected': False,
                'error': str(e),
                'scanner': 'error'
            }

    async def scan_with_clamav(self, file_path: str) -> Dict[str, Any]:
        """ClamAV bilan tekshirish"""
        try:
            # ClamAV ni ishga tushirish
            result = subprocess.run(
                [self.clamav_path, '--stdout', file_path],
                capture_output=True,
                text=True,
                timeout=30
            )

            output = result.stdout.lower()

            if 'found' in output or 'infected' in output:
                # Virus nomini ajratib olish
                virus_name = "Noma'lum"
                for line in output.split('\n'):
                    if 'found' in line or 'infected' in line:
                        parts = line.split(':')
                        if len(parts) > 1:
                            virus_name = parts[1].strip()
                        break

                return {
                    'is_infected': True,
                    'virus_name': virus_name,
                    'scanner': 'clamav',
                    'details': result.stdout
                }
            else:
                return {
                    'is_infected': False,
                    'scanner': 'clamav'
                }

        except subprocess.TimeoutExpired:
            return {
                'is_infected': False,
                'error': 'Timeout',
                'scanner': 'clamav'
            }
        except Exception as e:
            return {
                'is_infected': False,
                'error': str(e),
                'scanner': 'clamav'
            }

