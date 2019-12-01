USE [master]
GO
/****** Object:  Database [ARNutri]    Script Date: 12/1/19 3:09:21 PM ******/
CREATE DATABASE [ARNutri]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'ARNutri', FILENAME = N'/var/opt/mssql/data/ARNutri.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'ARNutri_log', FILENAME = N'/var/opt/mssql/data/ARNutri_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [ARNutri].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [ARNutri] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [ARNutri] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [ARNutri] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [ARNutri] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [ARNutri] SET ARITHABORT OFF 
GO
ALTER DATABASE [ARNutri] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [ARNutri] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [ARNutri] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [ARNutri] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [ARNutri] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [ARNutri] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [ARNutri] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [ARNutri] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [ARNutri] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [ARNutri] SET  ENABLE_BROKER 
GO
ALTER DATABASE [ARNutri] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [ARNutri] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [ARNutri] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [ARNutri] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [ARNutri] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [ARNutri] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [ARNutri] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [ARNutri] SET RECOVERY FULL 
GO
ALTER DATABASE [ARNutri] SET  MULTI_USER 
GO
ALTER DATABASE [ARNutri] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [ARNutri] SET DB_CHAINING OFF 
GO
ALTER DATABASE [ARNutri] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [ARNutri] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [ARNutri] SET DELAYED_DURABILITY = DISABLED 
GO
EXEC sys.sp_db_vardecimal_storage_format N'ARNutri', N'ON'
GO
ALTER DATABASE [ARNutri] SET QUERY_STORE = OFF
GO
USE [ARNutri]
GO
ALTER DATABASE SCOPED CONFIGURATION SET IDENTITY_CACHE = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION SET LEGACY_CARDINALITY_ESTIMATION = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET LEGACY_CARDINALITY_ESTIMATION = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET MAXDOP = 0;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET MAXDOP = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET PARAMETER_SNIFFING = ON;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET PARAMETER_SNIFFING = PRIMARY;
GO
ALTER DATABASE SCOPED CONFIGURATION SET QUERY_OPTIMIZER_HOTFIXES = OFF;
GO
ALTER DATABASE SCOPED CONFIGURATION FOR SECONDARY SET QUERY_OPTIMIZER_HOTFIXES = PRIMARY;
GO
USE [ARNutri]
GO
/****** Object:  Table [dbo].[Anthropometrics]    Script Date: 12/1/19 3:09:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Anthropometrics](
	[userId] [int] NULL,
	[heartBeats] [float] NOT NULL,
	[systolicPressure] [float] NOT NULL,
	[diastolicPressure] [float] NOT NULL,
	[weight] [float] NOT NULL,
	[height] [float] NOT NULL,
	[bmi] [float] NOT NULL,
	[armCircunference] [float] NOT NULL,
	[waistCircunference] [float] NOT NULL,
	[sagittalAbdominalDiameter] [float] NOT NULL,
	[fistStrength] [float] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Nutrients]    Script Date: 12/1/19 3:09:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Nutrients](
	[userId] [int] NULL,
	[calories] [float] NOT NULL,
	[proteins] [float] NOT NULL,
	[carbohydrates] [float] NOT NULL,
	[totalSugar] [float] NOT NULL,
	[fibers] [float] NOT NULL,
	[fats] [float] NOT NULL,
	[saturatedFat] [float] NOT NULL,
	[monounsaturatedFat] [float] NOT NULL,
	[polyunsaturatedFat] [float] NOT NULL,
	[cholesterol] [float] NOT NULL,
	[alcohol] [float] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[PersonalData]    Script Date: 12/1/19 3:09:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[PersonalData](
	[userId] [int] NULL,
	[age] [float] NOT NULL,
	[educationalLevel] [varchar](255) NOT NULL,
	[householdIncome] [float] NOT NULL,
	[totalPeopleResidence] [int] NOT NULL,
	[gender] [varchar](255) NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Socioeconomics]    Script Date: 12/1/19 3:09:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Socioeconomics](
	[userId] [int] NULL,
	[educationalLevel] [varchar](255) NOT NULL,
	[householdIncome] [float] NOT NULL
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 12/1/19 3:09:21 PM ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [varchar](255) NOT NULL,
	[gender] [varchar](255) NOT NULL,
	[email] [varchar](255) NOT NULL,
	[birth_date] [date] NOT NULL,
	[password] [varchar](255) NOT NULL,
	[medicalRegister] [varchar](255) NULL,
	[userType] [varchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
INSERT [dbo].[Anthropometrics] ([userId], [heartBeats], [systolicPressure], [diastolicPressure], [weight], [height], [bmi], [armCircunference], [waistCircunference], [sagittalAbdominalDiameter], [fistStrength]) VALUES (19, 123, 123, 123, 123, 123, 123, 123, 123, 123, 23)
INSERT [dbo].[Socioeconomics] ([userId], [educationalLevel], [householdIncome]) VALUES (12, N'4', 1200)
SET IDENTITY_INSERT [dbo].[Users] ON 

INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (1, N'Joao Carlos', N'Male', N'jcarlos@uol.com', CAST(N'1996-11-04' AS Date), N'senhaForte', N'', N'Pacient')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (3, N'Joao Paulo', N'Male', N'jramos@uol.com', CAST(N'1997-11-04' AS Date), N'pbkdf2:sha256:150000$VzQyRUir$113eecccb255e9a3fe5dabfaff58bd9de7e85ed0c5d8bf7ebfe7c3c1cb9ae9bd', N'', N'Pacient')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (9, N'Joao Carlos', N'Male', N'jarlos@uol.com', CAST(N'1996-11-04' AS Date), N'senhaForte', N'', N'Pacient')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (12, N'Bruna Paz', N'Female', N'ppaz@uol.com', CAST(N'1998-05-14' AS Date), N'pbkdf2:sha256:150000$SHXmYR59$40f57fc134c8ec9a8fe97771378a4291c6540e4c1a31a768d5683ee7d7fdb808', N'', N'Pacient')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (13, N'Joao', N'Male', N'jramos@fei.edu', CAST(N'1997-11-04' AS Date), N'pbkdf2:sha256:150000$CreqKqbU$c8d10d4501dde442082ed2c742e78058c42bbd5428f60133e7a8fc24a0fc2e8a', N'', N'Pacient')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (14, N'João Paulo ', N'Masculino', N'jramos@fei.com', CAST(N'1997-04-11' AS Date), N'pbkdf2:sha256:150000$ZQS1YbbE$b43e4295f12dca500c59059359bb0e3333622763afd5240d584e3403fd359c70', N'', N'Paciente')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (15, N'Jose', N'Masculino', N'jose@email.com', CAST(N'1900-01-01' AS Date), N'pbkdf2:sha256:150000$8XDwJgOv$82c95bd7efbe09bc9e4da66a3068324717e79fb00fad78134d04637c73280da8', N'12344', N'Médico')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (17, N'Josias', N'Masculino', N'josias@email.com', CAST(N'1900-01-01' AS Date), N'pbkdf2:sha256:150000$MORGo2Wj$46f2a2e8d2ee54c79c7c8424f751ae93390bddda55efafabb31e553806e04006', N'', N'Paciente')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (18, N'Jeremias', N'Masculino', N'jeremias@email.com', CAST(N'1900-01-02' AS Date), N'pbkdf2:sha256:150000$aXOJ2F2x$6a80cbe7ab250c6a3812053be8f2afe965c4e5cfc72ef92c25b541414b3912db', N'', N'Paciente')
INSERT [dbo].[Users] ([id], [name], [gender], [email], [birth_date], [password], [medicalRegister], [userType]) VALUES (19, N'Pinho', N'Masculino', N'pinho@email.com', CAST(N'1900-01-02' AS Date), N'pbkdf2:sha256:150000$n0VF96dF$8196aa87ba6180e628bca68d8ce0cbf0f06d281520a61b47df6529c69d046bb2', N'', N'Paciente')
SET IDENTITY_INSERT [dbo].[Users] OFF
SET ANSI_PADDING ON
GO
/****** Object:  Index [UQ__Users__AB6E61649E04CC64]    Script Date: 12/1/19 3:09:22 PM ******/
ALTER TABLE [dbo].[Users] ADD UNIQUE NONCLUSTERED 
(
	[email] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Anthropometrics]  WITH CHECK ADD FOREIGN KEY([userId])
REFERENCES [dbo].[Users] ([id])
GO
ALTER TABLE [dbo].[Nutrients]  WITH CHECK ADD FOREIGN KEY([userId])
REFERENCES [dbo].[Users] ([id])
GO
ALTER TABLE [dbo].[PersonalData]  WITH CHECK ADD FOREIGN KEY([userId])
REFERENCES [dbo].[Users] ([id])
GO
ALTER TABLE [dbo].[Socioeconomics]  WITH CHECK ADD FOREIGN KEY([userId])
REFERENCES [dbo].[Users] ([id])
GO
USE [master]
GO
ALTER DATABASE [ARNutri] SET  READ_WRITE 
GO
